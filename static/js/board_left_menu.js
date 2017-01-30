/**
 * Created by Родин Алексей on 12.01.2017.
 */
    $('#menu_list li').each(function () {
        $(this).remove('active')
    });
    $('#menu_list li a').each(function () {
        $(this).remove('toggled');
    });
    $('#menu_managers').addClass('active');

    
    $('#menu_users').addClass('toggled');
