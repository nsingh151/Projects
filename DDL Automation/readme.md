## Process for Introducing a New Entity

1. Create a Lucid Chart Model to present in Data Goverance call. For instance, [F_Payment_Transaction table Model](https://www.lucidchart.com/documents/edit/4e1f306c-b340-441f-a870-0e5d4d3e3a33/0) in Lucid chart.

2. Once Model is finalised , create a source to target mapping on your local machine taking this mapping as [standard document](https://github.com/nsingh151/Projects/blob/master/DDL%20Automation/test_source_to_target.xlsx).

3. Install the required packages listed in [requirements.txt file](https://github.com/nsingh151/Projects/blob/master/DDL%20Automation/requiremnets.txt.txt) using ``` pip install <package name> ``` or ``` pip install -r requirements.txt ```

4. Run [DDL Creation script](https://github.com/nsingh151/Projects/blob/master/DDL%20Automation/DDL_Creation_script.py)  using ``` python DDL_Creation_script.py ```
    - Script will ask for the Path where Source to Target mapping resides (**Note: Give complete path along with the file name For eg. : C:\Github\Projects\DDL Automation\test_source_to_target.xlsx**)
    - Script will ask the folder where you want to save Auto generated DDL (**Note: give complete path till the folder name file name will be auto added For illustration: C:\Github\BI_vdw\WARS\Facts**)
