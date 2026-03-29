int A = int.Parse(Console.ReadLine());
int B = int.Parse(Console.ReadLine());
int C = int.Parse(Console.ReadLine());

string result = (A * B * C).ToString();
int[] num = new int[10];

for (int i = 0; i < result.Length; i++)
{
    num[result[i] - '0']++;
}

for (int i = 0; i < num.Length; i++)
{
    Console.WriteLine(num[i]);
}
