function levenshteinDistance(a, b) {

  const ins_cost = 1; // insertion cost
  const del_cost = 1; // deletion cost
  const sub_cost = 1; // substitution cost

  a.unshift("#");
  b.unshift("#");

  var distanceMatrix = new Array(b.length).fill().map(() => Array(a.length).fill(0));
  //console.log(distanceMatrix);

  var edMatrix = new Array(b.length).fill().map(() => Array(a.length).fill(0));
  
  //initialize Matrices

  distanceMatrix[0][0] = 0;
  edMatrix[0][0] = "#";

  for (var i = 1; i < a.length; i++) {
    distanceMatrix[0][i] = i;
    edMatrix[0][i] = "I";
  }
  for (var j = 1; j < b.length; j++) {
    distanceMatrix[j][0] = j;
    edMatrix[j][0] = "D";
  }

  for (var j = 1; j < a.length; j++) {
    for (var i = 1; i < b.length; i++) {

      var cost1 = distanceMatrix[i][j-1] + ins_cost;
      var cost2 = distanceMatrix[i-1][j] + del_cost;
      
      var cost3 = null;
      if (a[j] == b[i]) {
        cost3 = distanceMatrix[i-1][j-1];
      } else {
        cost3 = distanceMatrix[i-1][j-1] + sub_cost;
      }

      if (Math.min(cost1, cost2, cost3) == cost3) {
        distanceMatrix[i][j] = cost3;
        edMatrix[i][j] = "R";
      } else if (Math.min(cost1, cost2, cost3) == cost2) {
        distanceMatrix[i][j] = cost2;
        edMatrix[i][j] = "D";
      } else {
        distanceMatrix[i][j] = cost1;
        edMatrix[i][j] = "I";
      }
    }
  }

  //console.log(distanceMatrix);

  // get edits
  j = a.length-1;
  i = b.length-1;
  var prev_edit = edMatrix[i][j];
  var edits = [prev_edit];
  while (prev_edit != "#") {
    if (prev_edit == "I") {
      prev_edit = edMatrix[i][j-1];
      j = j-1 ;
      edits.unshift("I");
    } else if (prev_edit == "D") {
      prev_edit = edMatrix[i-1][j];
      i = i-1;
      edits.unshift("D");
    } else {
      
        if (distanceMatrix[i][j] == distanceMatrix[i-1][j-1]) {
        edits.unshift("_");
      } else {
        edits.unshift("R");
      }
      prev_edit = edMatrix[i-1][j-1];
      j = j-1;
      i = i-1;
    }
  }

  var ed = parseInt(distanceMatrix[b.length-1][a.length-1]);
  edits.pop();
  return [ed, edits]
}

var res= levenshteinDistance("This is not a sentence.".split(" "), "This is a sentence.".split(" "));
console.log(res[0]);
console.log(res[1]);
console.log(res[1].includes('I'));