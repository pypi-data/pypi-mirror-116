#!/usr/bin/python3

import subprocess
import glob
import os
from rich.console import Console
from rich.table import Table
from rich.live import Live
from time import sleep
import argparse

console = Console()

def main():
	parser = argparse.ArgumentParser(description = 'A simple python utility script to update all github repositories in a location giving the user a good UI using the python rich module')
	parser.add_argument('-p', '--path', required = True, help = 'Path where all github repositories are located, Ex: /opt/source/')
	parser = parser.parse_args()
	path = parser.path

	table = Table()
	table.add_column("Project")
	table.add_column("Branch")
	table.add_column("Status")
	table.add_column("Comments")
	if path.split(os.path.sep)[-1] != '':
		os.path.sep.join(path.split(os.path.sep))
		path = f'{path}{os.path.sep}'
	folders = glob.glob(f'{path}*')
	
	success_count = 0
	fail_count = 0
	with console.status("[bold magenta]Initializing", spinner = "point", spinner_style = "magenta") as status:
		sleep(3)
		with Live(table) as live:
			for folder in folders:
				os.chdir(folder)
				if '.git' in glob.glob('.git'):
					branch = subprocess.check_output(['git', 'branch']).decode('utf-8').split('*')[1].split('\n')[0].lstrip()
					update = subprocess.run(['git', 'pull', 'origin', branch], shell=False, capture_output=True)
					if update.returncode == 0:
						success_count += 1
						table.add_row(folder.split("/")[3], branch, '[bold green]:heavy_check_mark:', '[bold green]successfully pulled the latest code')
					elif update.returncode == 1 and 'Permission denied' in update.stderr.decode('utf-8'):
						fail_count += 1
						table.add_row(folder.split("/")[3], branch, '[bold red]:heavy_multiplication_x:', '[bold red]permission denied')
					else:
						fail_count += 1
						table.add_row(folder.split("/")[3], branch, '[bold red]:heavy_multiplication_x:', '[bold red]error in pulling the latest code')
				else:
					fail_count += 1
					table.add_row(folder.split("/")[3], branch, '[bold yellow]:bangbang:', '[bold yellow]not a git repo')

				status.update(
					status = f"[bold magenta]Pulling code for {folder.split('/')[3]}",
					spinner = "bouncingBall",
					spinner_style = "magenta",
				)

	console.log(f'[#03ff91] Successfully pulled the latest code for {success_count} repos')
	console.log(f'[#03ff91] Failed to pull the latest code for {fail_count} repos')