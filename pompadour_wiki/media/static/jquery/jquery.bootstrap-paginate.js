(function($)
{
    $.fn.paginate = function(npages, perpage)
    {
        var pagination = this;

        var curpage = 0;
        var ocurpage = curpage;

        $('.pagination-page:first', this).addClass('active');
        $('.pagination-prev', this).addClass('disabled');

        $('.pagination-prev', this).click(function()
        {
            if (ocurpage != npages - 1)
            {
                $('.pagination-next', pagination).removeClass('disabled');
            }

            if (curpage - 1 == 0)
            {
                $('.pagination-prev', pagination).addClass('disabled');
            }
            else if (curpage - 1 < 0)
            {
                return false;
            }
            else
            {
                $('.pagination-prev', pagination).removeClass('disabled');
            }

            ocurpage = curpage;
            curpage = curpage - 1;

            $($('.pagination-page', pagination)[ocurpage]).removeClass('active');
            $($('.pagination-page', pagination)[curpage]).addClass('active');
        });

        $('.pagination-next', this).click(function()
        {
            if (ocurpage != 0)
            {
                $('.pagination-prev', pagination).removeClass('disabled');
            }

            if (curpage + 1 == npages - 1)
            {
                $('.pagination-next', pagination).addClass('disabled');
            }
            else if (curpage + 1 > npages - 1)
            {
                return false;
            }
            else
            {
                $('.pagination-next', pagination).removeClass('disabled');
            }

            ocurpage = curpage;
            curpage = curpage + 1;

            $($('.pagination-page', pagination)[ocurpage]).removeClass('active');
            $($('.pagination-page', pagination)[curpage]).addClass('active');
        });

        $('.pagination-page', this).click
    };
})(jQuery)
