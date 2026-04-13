class Program
{
    static void Main(string[] args)
    {
        while (true)
        {
            int sum = 0;
            int max = int.MinValue;

            int[] input = Array.ConvertAll(Console.ReadLine().Split(' '), int.Parse);

            if (input[0] == 0 && input[1] == 0 && input[2] == 0)
                break;

            for (int i = 0; i < input.Length; i++)
            {
                sum += input[i] * input[i];
                if (input[i] > max)
                    max = input[i];
            }

            if (sum - max * max == max * max)
                Console.WriteLine("right");
            else
                Console.WriteLine("wrong");
        }
    }
}
