import curses
import subprocess
import os
import sys

PREDEFINED_PACKAGES = [
    "vim", "git", "htop", "curl", "firefox",
    "neofetch", "tmux", "wget", "gcc", "make"
]
SWAP_SIZES = [2, 4, 8, 16]  # GB options

def run_command(command, stdscr=None, clear_screen=False, wait=True):
    if clear_screen and stdscr:
        stdscr.clear()
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ""
    for line in proc.stdout:
        if stdscr:
            stdscr.addstr(line.decode())
            stdscr.refresh()
        output += line.decode()
    proc.wait()
    if wait and stdscr:
        stdscr.addstr("\nPress any key to continue.")
        stdscr.refresh()
        stdscr.getch()
    return output

def get_disks():
    result = subprocess.run("lsblk -dn -o NAME,TYPE", shell=True, stdout=subprocess.PIPE)
    disks = []
    for line in result.stdout.decode().splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1] == "disk":
            disks.append(f"/dev/{parts[0]}")
    return disks

def check_disk_space(path="/"):
    st = os.statvfs(path)
    return st.f_bavail * st.f_frsize // (1024**3)  # GB available

def estimate_pkg_size(pkgs):
    # Basic estimate: 200MB per package (adjust as needed)
    return len(pkgs) * 0.2

def setup_swap(device, size_gb, stdscr):
    stdscr.clear()
    stdscr.addstr(1,2, f"Setting up {size_gb}GB swap on {device}...\n")
    stdscr.refresh()
    try:
        run_command(f"sudo dd if=/dev/zero of={device} bs=1G count={size_gb}", stdscr)
        run_command(f"sudo mkswap {device}", stdscr)
        run_command(f"sudo swapon {device}", stdscr)
        stdscr.addstr("Swap setup complete!\n")
    except Exception as e:
        stdscr.addstr(f"Error setting up swap: {e}\n")
    stdscr.refresh()
    stdscr.addstr("Press any key to continue.")
    stdscr.getch()

def install_packages(pkgs, stdscr):
    stdscr.clear()
    stdscr.addstr(1,2, f"Installing: {' '.join(pkgs)}\n")
    stdscr.refresh()
    try:
        run_command(f"sudo dnf install -y {' '.join(pkgs)}", stdscr)
        stdscr.addstr("Installation complete!\n")
    except Exception as e:
        stdscr.addstr(f"Error during install: {e}\n")
    stdscr.refresh()
    stdscr.addstr("Press any key to continue.")
    stdscr.getch()

def menu_list(stdscr, title, options, selected_idx=0):
    curses.curs_set(0)
    while True:
        stdscr.clear()
        stdscr.addstr(1,2,title)
        for idx, opt in enumerate(options):
            marker = "->" if idx == selected_idx else "  "
            stdscr.addstr(3+idx,4, f"{marker} {opt}")
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and selected_idx > 0:
            selected_idx -= 1
        elif key == curses.KEY_DOWN and selected_idx < len(options)-1:
            selected_idx += 1
        elif key in [10, 13]:
            return selected_idx

def checkbox_menu(stdscr, title, options, selected):
    curses.curs_set(0)
    idx = 0
    while True:
        stdscr.clear()
        stdscr.addstr(1,2,title)
        for i, opt in enumerate(options):
            checked = "[x]" if opt in selected else "[ ]"
            marker = "->" if i == idx else "  "
            stdscr.addstr(3+i,4, f"{marker} {checked} {opt}")
        stdscr.addstr(4+len(options),6, "Space: Toggle | Enter: Confirm | 'a': Add Custom")
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and idx > 0:
            idx -= 1
        elif key == curses.KEY_DOWN and idx < len(options)-1:
            idx += 1
        elif key == ord(' '):
            if options[idx] in selected:
                selected.remove(options[idx])
            else:
                selected.add(options[idx])
        elif key in [10, 13]:
            return selected
        elif key == ord('a'):
            stdscr.addstr(6+len(options),6, "Enter custom package name(s), separated by space: ")
            curses.echo()
            custom = stdscr.getstr(7+len(options),6,50).decode().strip()
            curses.noecho()
            if custom:
                for name in custom.split():
                    if name not in options:
                        options.append(name)
                    selected.add(name)

def confirm(stdscr, prompt):
    stdscr.clear()
    stdscr.addstr(2, 2, prompt)
    stdscr.addstr(4, 2, "Press 'y' to confirm, any other key to cancel.")
    stdscr.refresh()
    key = stdscr.getch()
    return key in [ord('y'), ord('Y')]

def final_fastfetch_and_delete():
    # Clear screen, run fastfetch, delete script, exit.
    os.system("clear")
    os.system("fastfetch")
    print("\nScript will now delete itself...")
    script_path = os.path.abspath(__file__)
    try:
        os.remove(script_path)
        print("Script deleted successfully.")
    except Exception as e:
        print(f"Failed to delete script: {e}")
    sys.exit(0)

def main(stdscr):
    # Run fastfetch at the start
    stdscr.clear()
    stdscr.addstr(1,2,"System Info (fastfetch):\n")
    stdscr.refresh()
    run_command("fastfetch", stdscr, wait=False)
    stdscr.addstr("\nPress any key to continue.")
    stdscr.refresh()
    stdscr.getch()
    stdscr.clear()
    
    # Swap Selection
    disks = get_disks()
    if not disks:
        stdscr.addstr(2,2,"No disks detected! Cannot setup swap.")
        stdscr.getch()
        return
    disk_idx = menu_list(stdscr, "Select disk for swap:", disks)
    swap_idx = menu_list(stdscr, "Select swap size (GB):", [str(s) for s in SWAP_SIZES])
    swap_device = disks[disk_idx]
    swap_size = SWAP_SIZES[swap_idx]
    stdscr.clear()
    
    # Package Selection
    selected_pkgs = set()
    selected_pkgs = checkbox_menu(stdscr, "Select packages to install:", PREDEFINED_PACKAGES.copy(), selected_pkgs)
    stdscr.clear()
    
    # Disk Space Check
    stdscr.addstr(1,2, f"Checking disk space...")
    root_space = check_disk_space("/")
    pkg_space_needed = estimate_pkg_size(selected_pkgs)
    total_needed = pkg_space_needed + swap_size
    stdscr.addstr(3,2, f"Estimated needed: {total_needed:.1f} GB | Available: {root_space:.1f} GB")
    if root_space < total_needed:
        stdscr.addstr(5,2, "Not enough disk space! Press any key to exit.")
        stdscr.refresh()
        stdscr.getch()
        return
    stdscr.addstr(5,2, "Enough space. Press any key to continue.")
    stdscr.refresh()
    stdscr.getch()
    
    # Run Setup
    setup_swap(swap_device, swap_size, stdscr)
    install_packages(list(selected_pkgs), stdscr)
    
    # Final fastfetch + self-delete
    if confirm(stdscr, "Delete this setup script from disk?"):
        curses.endwin() # Restore terminal before running fastfetch and deleting
        final_fastfetch_and_delete()
    else:
        stdscr.clear()
        stdscr.addstr(2,2,"Script NOT deleted. Press any key to exit.")
        stdscr.refresh()
        stdscr.getch()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Please run this script as root (sudo).")
        sys.exit(1)
    curses.wrapper(main)
