function buildtree(root, json, wiki)
{
    for(var i in json.node.children)
    {
        var node = json.node.children[i];

        if(node.node.type == 'tree')
        {
            var icon_folder = $('<i/>', { 'class': 'icon-folder-close' });

            var name = $('<li/>', { 'class': 'nav-header' });
            var link = $('<a/>', {'href': '/wiki/' + wiki + '/' + node.node.path, 'text': node.node.name });

            link.prepend(icon_folder);
            name.append(link);

            root.append(name);

            var new_root = $('<ul/>', { 'class': 'nav nav-list' });
            new_root.css('display', 'none');
            root.append(new_root);

            link.click(function(e)
            {
                if(e.target.nodeName == 'I')
                {
                    e.preventDefault();
                }
            });

            icon_folder.click(function()
            {
                var ul = $(this).parent().parent().next();
                ul.toggle('slow');

                if ($(this).hasClass('icon-folder-open'))
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
            var icon_file = $('<i/>', { 'class': 'icon-file' });

            var name = $('<li/>');
            var link = $('<a/>', {'href': '/wiki/' + wiki + '/' + node.node.path, 'text': node.node.name });

            link.prepend(icon_file);
            name.append(link);
            root.append(name);
        }
    }
}
