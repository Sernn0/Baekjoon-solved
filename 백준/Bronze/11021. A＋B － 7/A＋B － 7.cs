string[] input = Console.ReadLine().Split(' ');
int test_case = int.Parse(input[0]);
int[] result_arr = new int[test_case];

for (int i = 0; i < test_case; i++)
{
    string[] num_input = Console.ReadLine().Split(' ');
    int num1 = int.Parse(num_input[0]);
    int num2 = int.Parse(num_input[1]);
    result_arr[i] = num1 + num2;
}

for (int i = 1; i < test_case + 1; i++)
{
    Console.WriteLine($"Case #{i}: " + result_arr[i - 1]);
}
