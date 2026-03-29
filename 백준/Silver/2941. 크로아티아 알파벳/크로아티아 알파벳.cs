string input = Console.ReadLine();

string[] croatia_alphabet = { "c=", "c-", "dz=", "d-", "lj", "nj", "s=", "z=" };

foreach (string ca in croatia_alphabet)
{
    input = input.Replace(ca, "a");
}

Console.WriteLine(input.Length);
