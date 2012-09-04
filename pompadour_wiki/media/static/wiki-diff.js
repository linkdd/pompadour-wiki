if(typeof String.prototype.startsWith != 'function')
{
    String.prototype.startsWith = function (str)
    {
        return this.indexOf(str) == 0;
    };
}

function builddiff(element, json)
{
    for(var i in json.diffs)
    {
        var diff = json.diffs[i];

        var row = $('<tr/>');
        var msg = $('<td/>', {'text': diff.msg });
        var author = $('<td/>', {'text': diff.author });
        var date_ago = $('<td/>', {'text': $.timeago(new Date(diff.date * 1000))});

        row.append(msg);
        row.append(author);
        row.append(date_ago);

        row.click(diff.diff, function(jevent)
        {
            var lines = jevent.data.split('\n');
            var code = $('#diff');

            code.html('');

            for(var j in lines)
            {
                var line = lines[j];

                span = $('<span/>');

                // colorize diff with pygments code.css
                if(line.startsWith('diff') || line.startsWith('index'))
                {
                    span.addClass('gh');
                }
                else if(line.startsWith('@'))
                {
                    span.addClass('gu');
                }
                else if(line.startsWith('-'))
                {
                    span.addClass('gd');
                }
                else if(line.startsWith('+'))
                {
                    span.addClass('gi');
                }

                span.text(line);
                code.append(span);
                code.append('\n');
            }

            code.show('slow');
        });

        element.append(row);
    }
}
