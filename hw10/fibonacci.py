import tensorflow as tf

# define the recursion function
def recursion_fib(x):
    if x <= 1:
        return x
    else:
        return(recursion_fib(x-1) + recursion_fib(x-2))


with tf.Graph().as_default() as g:
    init = tf.global_variables_initializer()
    # find the number of fibbinacci numbers
    number = 30
    if number <= 0:
        print("A positive integer must be input")
    else:
        print("Fibonacci sequence:")
        for y in range(number):
            print("%d Fibonacci no.: %d" % (y,(recursion_fib(y))))
        tf.summary.FileWriter("logs", g).close()

exit()

