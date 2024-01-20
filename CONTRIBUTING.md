# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/dalwar23/kumaone/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

`kumaone` could always use more documentation, whether as part of the
official `kumaone` docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/dalwar23/kumanone/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started

Ready to contribute? Here's how to set up `kumaone` for local development.

1. Fork the `kumaone` repo on GitHub.
2. Clone your fork locally

    ```shell
    $ git clone git@github.com:your_name_here/kumaone.git
    ```
3. Install [pipenv](https://pipenv.pypa.io/en/latest/) from here.
4. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper
   installed, this is how you set up your fork for local development

   ```shell
   $ cd kumaone/
   $ pipenv shell
   $ pipenv install --dev
   $ pipenv install -e .
   ```
5. Create a branch for local development

   ```shell
   $ git checkout -b name-of-your-bugfix-or-feature
   ```
   Now you can make your changes locally.
6. When you're done making changes, check that your changes pass `black` formatting
   and behaves as expected.

   ```shell
   black src/kumaone
   ```
7. Commit your changes and push your branch to GitHub

   ```shell
   $ git add .
   $ git commit -m "Your detailed description of your changes."
   $ git push origin name-of-your-bugfix-or-feature
   ```
8. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list of TODO in README file.
2. The pull request should work for Python 3.8, 3.9, 3.10 > 3.10 and for PyPy.

