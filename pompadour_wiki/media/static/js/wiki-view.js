(function ($)
{
     $.fn.wikiView = function ()
     {
          $('.wiki-view-content').show ();
          $('.wiki-view-attachements').hide ();

          $('.wiki-view-arrow').click (function ()
          {
               $('.wiki-view-attachements').toggle ('slow');
          });
     };
}) (jQuery);
