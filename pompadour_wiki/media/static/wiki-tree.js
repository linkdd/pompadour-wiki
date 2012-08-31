function buildtree(root, json, wiki)
{
    for(var i in json.node.children)
    {
        var node = json.node.children[i];

        if(node.node.type == 'tree')
        {
            var icon_folder = $('<i/>', { 'class': 'icon-folder-close', 'style': 'float: left;' });

            var name = $('<li/>', { 'class': 'nav-header' });
            name.append(icon_folder);
            name.append($('<a/>', {'href': '/wiki/' + wiki + '/' + node.node.path, 'text': node.node.name }));

            root.append(name);

            var new_root = $('<ul/>', { 'class': 'nav nav-list' });
            new_root.css('display', 'none');
            root.append(new_root);

            icon_folder.click(function()
            {
                var ul = $(this).parent().next();
                ul.toggle('slow');

                if (ul.css('display') == 'none')
                {
                    $(this).removeClass('icon-folder-open');
                    $(this).addClass('icon-folder-close');
                }
                else
                {
                    $(this).removeClass('icon-folder-close');
                    $(this).addClass('icon-folder-open');
                }
            });

            buildtree(new_root, node, wiki);
        }
        else
        {
            var icon_file = $('<i/>', { 'class': 'icon-file', 'style': 'float: left;' });

            var name = $('<li/>');
            name.append(icon_file);
            name.append($('<a/>', {'href': '/wiki/' + wiki + '/' + node.node.path, 'text': node.node.name }));
            root.append(name);
        }
    }
}
