class Program
{
    static void Main(string[] args)
    {
        float[] input = Array.ConvertAll(Console.ReadLine().Split(' '), float.Parse);

        Console.WriteLine(Math.Ceiling(input[0] / input[1]));
    }
}
