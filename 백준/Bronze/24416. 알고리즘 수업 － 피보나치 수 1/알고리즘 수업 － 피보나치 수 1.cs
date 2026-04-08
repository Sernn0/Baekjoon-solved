class Program
{
    static int fibCounter = 1;

    static int Fib(int n)
    {
        if (n == 1 || n == 2)
        {
            return 1;
        }
        else
        {
            fibCounter++;
            return Fib(n - 1) + Fib(n - 2);
        }
    }

    static int Fibonacci(int n)
    {
        int counter = 0;

        int[] f = new int[n + 1];
        f[0] = 1;
        f[1] = 1;

        for (int i = 2; i < n; i++)
        {
            f[i] = f[i - 1] + f[i - 2];
            counter++;
        }

        return counter;
    }

    static void Main(string[] args)
    {
        int input = int.Parse(Console.ReadLine());
        Fib(input);
        Console.WriteLine($"{fibCounter} {Fibonacci(input)}");
    }
}
