function check(field) {
    var v = field.value.charAt(field.value.length - 1);
    if (v >= '9' || v <= '0') {
        field.value = field.value.substring(0, field.value.length - 1);
    }
}

/*
<form>
    <input type="text" onkeypress="check(this);" />
</form>
*/
