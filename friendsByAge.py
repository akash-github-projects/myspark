from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("friendsByAge")
sc = SparkContext(conf=conf)


def parse_line(line):
    fields = line.split(',')

    age = int(fields[2])
    num_friends = int(fields[3])

    return age, num_friends


lines = sc.textFile("data/friends.data")
rdd = lines.map(parse_line)

total_by_age = rdd.mapValues(lambda x: (x, 1)).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
average_by_age = total_by_age.mapValues(lambda x: x[0] / x[1])

results = average_by_age.collect()

for result in results:
    print(result)
