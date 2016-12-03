var Suggest = function (name, tlds) {
    // suggest an ending based on the edit distance
    var _ending = Suggest.ending(name, 3, tlds);

    // get the endings and the head (remaining thing).
    var head = _ending[1];
    var endings = _ending[0];

    // and join them again
    return Suggest.join(head, endings);
};

Suggest.ending = function(name, max_distance, tlds){
    // get the list of tokens
    var tokens = name.split(/[^aA-zZ0-9]+/).map(function(e){return e.trim(); });

    // split into right tail and right head
    var rtail = tokens.slice(0, tokens.length - 1);
    var rhead = tokens[tokens.length - 1];

    var distances = tlds.map(function(e){return [e, Suggest.editDistance(e, rhead)];});
    distances.sort(function(a, b){return a[1]-b[1];});

    var valid = distances.filter(function(e){return e[1] < max_distance;}).map(function(e){return e[0]; });

    if(valid.length == 0){
        valid = ['com', 'net', 'org', 'io', 'tk'];
        rtail = tokens;
    }


    return [valid, rtail];
};

Suggest.join = function(tail, ending){
    var results = [];

    for(var e = 0; e < ending.length; e++){
        results.push(tail.join('-') + "." + ending[e]);
    }

    return results;
};


/**
 * Computes the edit distance between two strings.
 * @param a
 * @param b
 * @returns {*}
 */
Suggest.editDistance = function (a, b) {
    /*
     Copyright (c) 2011 Andrei Mackenzie
     Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
     The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
     */
    if (a.length == 0) return b.length;
    if (b.length == 0) return a.length;

    var matrix = [];

    // increment along the first column of each row
    var i;
    for (i = 0; i <= b.length; i++) {
        matrix[i] = [i];
    }

    // increment each column in the first row
    var j;
    for (j = 0; j <= a.length; j++) {
        matrix[0][j] = j;
    }

    // Fill in the rest of the matrix
    for (i = 1; i <= b.length; i++) {
        for (j = 1; j <= a.length; j++) {
            if (b.charAt(i - 1) == a.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(matrix[i - 1][j - 1] + 1, // substitution
                    Math.min(matrix[i][j - 1] + 1, // insertion
                        matrix[i - 1][j] + 1)); // deletion
            }
        }
    }

    return matrix[b.length][a.length];
};
