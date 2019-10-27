var nums = [19, 19, 19, 19]
var result = 41
var final_equation = ""
// var cnt = 0

function dfs(nums, equation) {
    if(nums.length <= 0){
        r = eval(equation) == result
        //console.log(equation)
        // cnt++
        if(r) {
            final_equation = equation
        }
        return r
    }
    for(var i=0; i < nums.length; i++) {
        var new_nums = [...nums]
        new_nums.splice(i, 1)
        var cur_num = nums[i].toString()
        if(equation == ""){
            return dfs(new_nums, cur_num)
        }
        else {
            if(dfs(new_nums, equation + "+" + cur_num)) return true
            if(dfs(new_nums, "~(" + equation + ")" + "+" + cur_num)) return true
            if(dfs(new_nums, equation + "+" + "~" + cur_num )) return true
            if(dfs(new_nums, "~(" + equation + ")" + "+" + "~" + cur_num)) return true
            
            if(dfs(new_nums, equation + "-" + cur_num)) return true
            if(dfs(new_nums, "~(" + equation + ")" + "-" + cur_num)) return true
            if(dfs(new_nums, equation + "-" + "~" + cur_num)) return true
            if(dfs(new_nums, "~(" + equation + ")" + "-" + "~" + cur_num)) return true

            if(dfs(new_nums, equation + "&" + cur_num)) return true
            if(dfs(new_nums, "~(" + equation + ")" + "&" + cur_num)) return true
            if(dfs(new_nums, equation + "&" + "~" + cur_num)) return true
            if(dfs(new_nums, "~(" + equation + ")" + "&" + "~" + cur_num )) return true

            if(dfs(new_nums, equation + "|" + cur_num)) return true
            if(dfs(new_nums, "~(" + equation + ")" + "|" + cur_num)) return true
            if(dfs(new_nums, equation + "|" + "~" + cur_num)) return true
            if(dfs(new_nums, "~(" + equation + ")" + "|" + "~" + cur_num)) return true
        }
    }
    return false
}

// r = dfs(nums,"")
// console.log(r, final_equation, cnt)
