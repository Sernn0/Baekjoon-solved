class Program
{
    static void Main(string[] args)
    {
        string[] input = Console.ReadLine().Split(' ');
        int N = int.Parse(input[0]);
        int K = int.Parse(input[1]);
        int[] track = Array.ConvertAll(Console.ReadLine().Split(' '), int.Parse);

        int counter = 0;

        for (int i = 1; i < N; i++)
        {
            if (track[i] <= track[i - 1])
            {
                track[i] += K;
                if (track[i] > track[i - 1])
                    counter++;
                else
                {
                    counter = -1;
                    break;
                }
            }
        }
        Console.WriteLine(counter);
    }
}
