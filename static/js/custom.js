
function submitSource(id)
{

    $('#form'+id).submit();
}

function submitCategory(id)
{

    $('#form'+id).submit();
}

function sourceSelect(id) {
    $('#selectSourceForm'+id).submit();
}

function categorySelected(cat,count)
{

   $('#categoryForm'+count).submit();
}

function languageSelected(id,count) {

    $('#languageSelectedForm'+count).submit();
}