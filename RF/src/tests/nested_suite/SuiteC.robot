*** Settings ***
Library    Collections
Test Tags       requirement: 42    smoke
Metadata    @TSCID1109    true
Metadata    @author    stefan923

*** Variables ***
${GLOBAL_VAR1}    This is a global variable!
@{LETTERS}    a  b  c  d  e  f  g  h  i  j  k  l  m  n  o  p  q  r  s  t  u  v  w  x  y  z

*** Test Cases ***
Test Case 1
    [Tags]    not ready
    [Documentation]    @TSCID1109: Verify login functionality
    Log    Test Case 1
    Log     ${GLOBAL_VAR1}
    Sleep   3s

Test Case 2
    Log    Test Case 2
    Log Many    @{LETTERS}
    Sleep   3s

Test Case 3
    Log    Test Case 3
    Sleep   3s