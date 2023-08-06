import os
from subprocess import call


def main():
    os.environ["CMDSTAN"] = f"{os.getcwd()}/cmdstan_builder/stan/cmdstan-2.27.0"
    os.environ["STAN_BACKEND"] = "CMDSTANPY"
    print(f'CMDSTAN location: {os.getenv("CMDSTAN")}')
    call('pip install prophet==1.0.1', shell=True)
    call('pip uninstall pystan -y', shell=True)
    print("PyStan uninstalled")
