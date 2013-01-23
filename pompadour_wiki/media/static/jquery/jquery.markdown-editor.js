String.prototype.splice = function(idx, rem, s)
{
    return (this.slice(0,idx) + s + this.slice(idx + Math.abs(rem)));
};

(function($)
{
    $.fn.insertCurline = function(action, string)
    {
        var content = $(this).val();
        var pos = $(this).getSelectionStart();

        if (action == 'before' || action == 'after')
        {
            var lines = content.split('\n');

            var sz = 0;
            var i = 0;

            while (i < lines.length)
            {
                sz += 1;

                if ((sz + lines[i].length) > pos)
                {
                    break;
                }

                sz += lines[i].length;
                ++i;
            }

            if (action == 'before')
            {
                lines[i] = string + lines[i];
            }
            else
            {
                lines[i] += string;
            }

            content = lines.join('\n');
            $('.markup-content').val(content);
        }
    };

    $.fn.getSelectionStart = function()
    {
        return $(this)[0].selectionStart;
    };

    $.fn.getSelectionEnd = function()
    {
        return $(this)[0].selectionEnd;
    };

    $.fn.select = function(begin, end)
    {
        $(this)[0].selectionStart = begin;
        $(this)[0].selectionEnd = end;
    };

    $.fn.markdownize = function ()
    {
        $('.markup').click(function()
        {
            if ($(this).hasClass('markup-h1'))
            {
                $('.markup-content').insertCurline('before', '# ');
            }
            else if ($(this).hasClass('markup-h2'))
            {
                $('.markup-content').insertCurline('before', '## ');
            }
            else if ($(this).hasClass('markup-h3'))
            {
                $('.markup-content').insertCurline('before', '### ');
            }
            else if ($(this).hasClass('markup-h4'))
            {
                $('.markup-content').insertCurline('before', '#### ');
            }
            else if ($(this).hasClass('markup-h5'))
            {
                $('.markup-content').insertCurline('before', '##### ');
            }
            else if ($(this).hasClass('markup-h6'))
            {
                $('.markup-content').insertCurline('before', '###### ');
            }

            else if ($(this).hasClass('markup-list'))
            {
                $('.markup-content').insertCurline('before', '* ');
            }
            else if ($(this).hasClass('markup-nlist'))
            {
                $('.markup-content').insertCurline('before', '1. ');
            }

            else if ($(this).hasClass('markup-quote'))
            {
                $('.markup-content').insertCurline('before', '> ');
            }
            else if ($(this).hasClass('markup-code'))
            {
                $('.markup-content').insertCurline('before', '    ');
            }

            else if ($(this).hasClass('markup-bold'))
            {
                var begin = $('.markup-content').getSelectionStart();
                var end = $('.markup-content').getSelectionEnd();
                var content = $('.markup-content').val();

                if (begin == end)
                {
                    var token = '** your bold text here **';

                    $('.markup-content').val(content.splice(begin, 0, token));

                    $('.markup-content').select(begin + 2, begin + 2 + token.length - 4);
                }
                else
                {
                    content = content.splice(begin, 0, '**');
                    content = content.splice(end + 2, 0, '**');
                    $('.markup-content').val(content);
                }
            }
            else if ($(this).hasClass('markup-italic'))
            {
                var begin = $('.markup-content').getSelectionStart();
                var end = $('.markup-content').getSelectionEnd();
                var content = $('.markup-content').val();

                if (begin == end)
                {
                    var token = '** your italic text here *';

                    $('.markup-content').val(content.splice(begin, 0, token));

                    $('.markup-content').select(begin + 1, begin + 1 + token.length - 2);
                }
                else
                {
                    content = content.splice(begin, 0, '*');
                    content = content.splice(end + 1, 0, '*');
                    $('.markup-content').val(content);
                }
            }

            else if ($(this).hasClass('markup-link'))
            {
                var begin = $('.markup-content').getSelectionStart();
                var content = $('.markup-content').val();
                var token = '[my link](http://)';

                $('.markup-content').val(content.splice(begin, 0, token));
                $('.markup-content').select(begin + 10, begin + token.length - 1);

            }
            else if ($(this).hasClass('markup-picture'))
            {
                var begin = $('.markup-content').getSelectionStart();
                var content = $('.markup-content').val();
                var token = '![alt text](http://)';

                $('.markup-content').val(content.splice(begin, 0, token));
                $('.markup-content').select(begin + 12, begin + token.length - 1);

            }
        });
    };
})(jQuery);
