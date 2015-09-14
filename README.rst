TomatoCart - Shopping cart
==========================

`TomatoCart`_ covers most of the features a shopping cart must have, and
more: Site Mangement , Catalog Management and Browsing, Product
Management and Browsing, Customer Management, Order Management, Payment,
Shipping, Checkout, Statistics and Reports, Promotion tools and SEO,
Content Management System.

This appliance includes all the standard features in `TurnKey Core`_,
and on top of that:

- TomatoCart configurations:
   
   - Installed from upstream source code to /var/www/tomatocart

- SSL support out of the box.
- `Adminer`_ administration frontend for MySQL (listening on port
  12322 - uses SSL).
- Postfix MTA (bound to localhost) to allow sending of email (e.g.,
  password recovery).
- Webmin modules for configuring Apache2, PHP, MySQL and Postfix.

Credentials *(passwords set at first boot)*
-------------------------------------------

-  Webmin, SSH, MySQL, Adminer: username **root**
-  TomatoCart: username **admin**


.. _TomatoCart: http://www.tomatocart.com
.. _TurnKey Core: https://www.turnkeylinux.org/core
.. _Adminer: http://www.adminer.org/
