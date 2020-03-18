var array = [1,2,3,4,5,6,7,8,9,10];
console.log(array);
for(i = array.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = array[i];
    array[i] = array[j];
    array[j] = tmp;
}
console.log(array);

