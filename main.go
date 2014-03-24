package main

import (
	"database/sql"
	"flag"
	"fmt"
	"github.com/fzzy/radix/redis"
	_ "github.com/lib/pq"
	"log"
	"math/rand"
	"os"
	"os/signal"
	"strings"
	"sync/atomic"
	"time"
)

const (
	OpRead  uint8 = 1
	OpWrite uint8 = 2
)

type Counter struct {
	values [2]uint32
	active int
}

func NewCounter() *Counter {
	const interval = 5

	c := &Counter{}

	go func() {
		timer := time.Tick(interval * time.Second)
		for _ = range timer {
			atomic.StoreUint32(&c.values[1-c.active], 0)
			c.active = 1 - c.active
			fmt.Printf("%6d req/sec\n", c.values[1-c.active]/interval)
		}
	}()

	return c
}

func (c *Counter) Increment() {
	atomic.AddUint32(&c.values[c.active], 1)
}

type Task struct {
	Op    uint8
	Key   string
	Field string
	Value string
}

func RedisClient() *redis.Client {
	client, err := redis.Dial("tcp", "localhost:6379")
	if err != nil {
		log.Fatal(err)
	}

	return client
}

func PgClient() *sql.DB {
	db, err := sql.Open("postgres", "user=student dbname=student sslmode=disable host=/var/run/postgresql")
	if err != nil {
		log.Fatal(err)
	}

	return db
}

func RedisWorker(input <-chan *Task, done chan<- struct{}, counter *Counter) {
	client := RedisClient()

	for task := range input {
		if task.Op == OpWrite {
			client.Cmd("HSET", task.Key, task.Field, task.Value)
		} else if task.Op == OpRead {
			reply := client.Cmd("HGET", task.Key, task.Field)
			val, err := reply.Str()
			if err != nil {
				log.Fatal(err)
			}
			if !strings.HasSuffix(val, task.Value) {
				log.Fatal(val, task.Value, task)
			}
		}
		counter.Increment()
	}

	client.Close()
	done <- struct{}{}
}

func PgWorker(input <-chan *Task, done chan<- struct{}, counter *Counter) {
	db := PgClient()

	for task := range input {
		if task.Op == OpWrite {
			_, err := db.Exec("SELECT upsert_data_"+task.Field+"($1, $2);", task.Key, task.Value)
			if err != nil {
				log.Fatal(err)
			}
		} else if task.Op == OpRead {
			row := db.QueryRow("SELECT "+task.Field+" FROM data WHERE id = $1", task.Key)
			var val string
			err := row.Scan(&val)
			if err != nil {
				log.Fatal(err)
			}
			if !strings.HasSuffix(val, task.Value) {
				log.Fatal(val, task.Value, task)
			}
		}
		counter.Increment()
	}

	db.Close()
	done <- struct{}{}
}

var stop = false

func SigHandler() {
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)

	go func() {
		<-c
		stop = true
		fmt.Printf("Stopping...\n")
	}()
}

func main() {
	var (
		workers, numObjects, writePercent int
		mode                              string
	)
	flag.IntVar(&workers, "workers", 4, "number of parallel workers")
	flag.IntVar(&numObjects, "num_objects", 100000, "number of objects")
	flag.StringVar(&mode, "mode", "redis", "operation mode: redis|postgres")
	flag.IntVar(&writePercent, "write_percent", 30, "percent of write operations in rw phase")
	flag.Parse()

	SigHandler()

	if mode == "redis" {
		client := RedisClient()
		client.Cmd("FLUSHALL")
		client.Close()
	} else if mode == "postgres" {
		db := PgClient()
		_, err := db.Exec("TRUNCATE data")
		if err != nil {
			log.Fatal(err)
		}
		db.Close()
	} else {
		log.Fatal("unknown mode")
	}

	counter := NewCounter()

	queue := make(chan *Task, 1000)
	done := make(chan struct{})

	for i := 0; i < workers; i++ {
		if mode == "postgres" {
			go PgWorker(queue, done, counter)
		} else {
			go RedisWorker(queue, done, counter)
		}
	}

	for i := 0; i < numObjects && !stop; i++ {
		for j := 0; j < 10 && !stop; j++ {
			queue <- &Task{Op: OpWrite, Key: fmt.Sprintf("obj%d", i), Field: fmt.Sprintf("f%d", j), Value: fmt.Sprintf("xx%d.%d", i, j)}
		}
	}

	fmt.Printf("Going r/w\n")

	for !stop {
		op := OpRead
		i, j := rand.Int31n(int32(numObjects)), rand.Int31n(10)
		if int(rand.Int31n(100)) < writePercent {
			op = OpWrite
		}
		queue <- &Task{Op: op, Key: fmt.Sprintf("obj%d", i), Field: fmt.Sprintf("f%d", j), Value: fmt.Sprintf("%d.%d", i, j)}
	}

	close(queue)

	for i := 0; i < workers; i++ {
		<-done
	}
}
