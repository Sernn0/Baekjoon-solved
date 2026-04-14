class Program
{
    static void Main(string[] args)
    {
        int N = int.Parse(Console.ReadLine());
        //S, M, L, XL, XXL, XXXL -> 6개 항목
        int[] input = Array.ConvertAll(Console.ReadLine().Split(' '), int.Parse);
        string[] TP = Console.ReadLine().Split(' ');

        int T = int.Parse(TP[0]);
        int P = int.Parse(TP[1]);

        int counter = 0;

        for (int i = 0; i < input.Length; i++)
        {
            while (input[i] > 0)
            {
                input[i] -= T;
                counter++;
            }
        }
        Console.WriteLine(counter);
        Console.WriteLine($"{N / P} {N % P}");
    }
}
