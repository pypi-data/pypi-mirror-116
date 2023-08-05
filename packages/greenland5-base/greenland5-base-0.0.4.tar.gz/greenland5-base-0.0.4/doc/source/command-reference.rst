Command Reference
=================

``greenland bist``
------------------

Running All Tests
.................

``greenland bist`` without any additional parameters runs the built-in
self tests of all Greenland5 packages that are currently installed, e.g.


.. code-block:: console

   $ greenland bist		

   => Running: greenland.metaprogramming.tests
   ============== test session starts ================================================
   platform linux -- Python 3.9.6, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
   rootdir: /secure/user/mel/archlinux-1/home/.work/my/greenland5/metaprogramming/src/greenland/metaprogramming/tests, configfile: pytest.ini
   collected 7 items                                                                                                                                                           

   test_inheritable_declarators.py .......                                      [100%]

   ============== 7 passed in 0.03s ==================================================

   => Running: greenland.infrastructure.tests
   ============== test session starts ================================================
   platform linux -- Python 3.9.6, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
   rootdir: /secure/user/mel/archlinux-1/home/.work/my/greenland5/infrastructure/src/greenland/infrastructure/tests, configfile: pytest.ini
   collected 5 items                                                                                                                                                           

   test_callerinfo.py ..                                                        [ 40%]
   test_mro.py ..                                                               [ 80%]
   test_tracing.py .                                                            [100%]

   ============ 5 passed in 0.09s ====================================================


Note the following:

- The output has been edited to fit within the page margins.
- The tests actually run depend on the Greenland5 packages actually
  installed. In the case shown above two built-in self test suites
  exist: ``greenland.metaprogramming.tests`` and
  ``greenland.infrastructure.tests``.

Running Only Selected Tests
...........................
  
``greenland bist`` *testname(s)* will run the test suites named in the arguments, e.g.:

.. code-block:: console

   $ greenland bist greenland.metaprogramming.tests
   
   => Tests to be run: ['greenland.metaprogramming.tests']

   => Running: greenland.metaprogramming.tests
   ============= test session starts =================================================
   platform linux -- Python 3.9.6, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
   rootdir: /secure/user/mel/archlinux-1/home/.work/my/greenland5/metaprogramming/src/greenland/metaprogramming/tests, configfile: pytest.ini
   collected 7 items                                                                                                                                                           

   test_inheritable_declarators.py .......                                      [100%]

   ============= 7 passed in 0.03s ===================================================


