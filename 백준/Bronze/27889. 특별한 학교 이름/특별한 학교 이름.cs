class Program
{
    static void Main(string[] args)
    {
        Dictionary<string, string> univ = new Dictionary<string, string>();
        univ["NLCS"] = "North London Collegiate School";
        univ["BHA"] = "Branksome Hall Asia";
        univ["KIS"] = "Korea International School";
        univ["SJA"] = "St. Johnsbury Academy";

        string input = Console.ReadLine();

        Console.WriteLine(univ[input]);
    }
}
