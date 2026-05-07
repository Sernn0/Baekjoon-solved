function solution(arr, delete_list) {
    answer = arr.filter(num => !(delete_list.includes(num)))
    return answer;
}