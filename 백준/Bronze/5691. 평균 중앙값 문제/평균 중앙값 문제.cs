class Program
{
    static void Main(string[] args)
    {
        while (true)
        {
            int[] input = Array.ConvertAll(Console.ReadLine().Split(' '), int.Parse);
            int A = input[0];
            int B = input[1];

            if (input[0] == 0 && input[1] == 0)
                break;
            else
            {
                int C = A * 2 - B;
                Console.WriteLine(C);
            }
        }
    }
}
