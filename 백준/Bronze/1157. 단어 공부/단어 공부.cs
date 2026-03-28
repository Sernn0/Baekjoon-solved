string input = Console.ReadLine().ToUpper();
int[] alphabet = new int[26];
int most_char = int.MinValue;
int most_reminder = 0;
int counter = 0;

for (int i = 0; i < input.Length; i++)
{
    switch (input[i])
    {
        case 'A':
            alphabet[0] += 1;
            break;
        case 'B':
            alphabet[1] += 1;
            break;
        case 'C':
            alphabet[2] += 1;
            break;
        case 'D':
            alphabet[3] += 1;
            break;
        case 'E':
            alphabet[4] += 1;
            break;
        case 'F':
            alphabet[5] += 1;
            break;
        case 'G':
            alphabet[6] += 1;
            break;
        case 'H':
            alphabet[7] += 1;
            break;
        case 'I':
            alphabet[8] += 1;
            break;
        case 'J':
            alphabet[9] += 1;
            break;
        case 'K':
            alphabet[10] += 1;
            break;
        case 'L':
            alphabet[11] += 1;
            break;
        case 'M':
            alphabet[12] += 1;
            break;
        case 'N':
            alphabet[13] += 1;
            break;
        case 'O':
            alphabet[14] += 1;
            break;
        case 'P':
            alphabet[15] += 1;
            break;
        case 'Q':
            alphabet[16] += 1;
            break;
        case 'R':
            alphabet[17] += 1;
            break;
        case 'S':
            alphabet[18] += 1;
            break;
        case 'T':
            alphabet[19] += 1;
            break;
        case 'U':
            alphabet[20] += 1;
            break;
        case 'V':
            alphabet[21] += 1;
            break;
        case 'W':
            alphabet[22] += 1;
            break;
        case 'X':
            alphabet[23] += 1;
            break;
        case 'Y':
            alphabet[24] += 1;
            break;
        case 'Z':
            alphabet[25] += 1;
            break;
    }
}

for (int i = 0; i < 26; i++)
{
    if (alphabet[i] > most_char)
    {
        most_char = alphabet[i];
        most_reminder = 65 + i;
    }
}

for (int i = 0; i < 26; i++)
{
    if (alphabet[i] == most_char)
    {
        counter += 1;
    }
}

if (counter == 1)
    Console.WriteLine((char)most_reminder);
else
    Console.WriteLine("?");
