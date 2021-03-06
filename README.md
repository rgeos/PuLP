This is a very simple analysis of the US Presidential Elections intended to minimize the % of the total population
needed in order to win the elections.

The application is build with Flask and it used PuLP library for optimization.

Python libraries requirements:
- Flask (http://flask.pocoo.org/)
- Flask_SQLalchemy (http://flask-sqlalchemy.pocoo.org)
- PuLP (https://github.com/coin-or/pulp)
- Python 3.6 or above

Linear Programming solvers requirements (at least one):  
- CBC (https://projects.coin-or.org/Cbc)
- GLPK (https://www.gnu.org/software/glpk/)
- Other solvers https://en.wikipedia.org/wiki/Linear_programming#Solvers_and_scripting_(programming)_languages

How to use:
1. Download the repository locally `git clone git@github.com:rgeos/PuLP.git`
2. `cd PuLP`
3. Run the application with `python main.py run`
4. Access the application via web browser `localhost:8001`

API access points:
1. `localhost:8001/opt1` - bin assignment problem
2. `localhost:8001/opt2/0` - knapsack problem version 1
3. `localhost:8001/opt2/1` - knapsack problem version 2

For details on the above API access points check the blog at [this link](https://blog.epigno.systems/2017/12/10/operations-research-and-us-elections/).