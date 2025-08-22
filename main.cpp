// Pause between checks
#include <thread>
#include <chrono>

// Getting app names
#include <windows.h>
#include <psapi.h>

// Printing out/main functionality
#include <iostream>
#include <string>

// Collecting/storing data
#include <map>
#include <vector>
#include <algorithm>

// Saving to file
#include <fstream>

// Manipulating with time
#include <ctime>
#include <iomanip>

using namespace std;

string changeTimeFormat(int totalSeconds)
/*
Function that formats the time from seconds -> HH:MM:SS
*/
{
    // Calculate all the variables
    int hours = totalSeconds / 3600;
    int minutes = (totalSeconds % 3600) / 60;
    int secs = totalSeconds % 60;


    // Format it
    ostringstream oss;
    oss << setw(2) << setfill('0') << hours << ":"
        << setw(2) << setfill('0') << minutes << ":"
        << setw(2) << setfill('0') << secs;

    return oss.str(); // Return it
}

string getTime()
/*
Function that returns current time
*/
{
    // Gets current time
    auto now = chrono::system_clock::now();
    time_t now_time = chrono::system_clock::to_time_t(now);


    // Formats it and returns it
    char buf[20];
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", localtime(&now_time));
    return string(buf);
}

string getDay(){
    // Gets current time
    auto now = chrono::system_clock::now();
    time_t now_time = chrono::system_clock::to_time_t(now);


    // Formats it and returns it
    char buf[11];
    strftime(buf, sizeof(buf), "%Y-%m-%d", localtime(&now_time));
    return string(buf);
}

void saveData(const map<string, int> &base, const map<string, string> &times)
/*
Function that is used to save data to log_%Y-%m-%d.csv
*/
{
    string filename = "logs/log_" + getDay() + ".csv";
    ofstream outFile(filename, ios::trunc); // Opens a file

    for (auto &it : base)
    {
        string app = it.first; // App name
        int totalTime = it.second; // App time in seconds

        string lastTime = ""; // Last time usage
        auto tIt = times.find(app);
        if (tIt != times.end())
        {
            lastTime = tIt->second; // Save last time usage to its variable
        }

        outFile << app << "," << changeTimeFormat(totalTime) << "," << lastTime << endl; // Save it all in
    }

    outFile.close(); // Close a file
}

string getFileName(const string &fullPath)
/*
Function that is used to get just file name from a file path
*/
{
    size_t pos = fullPath.find_last_of("\\/");
    if (pos == std::string::npos)
        return fullPath;
    return fullPath.substr(pos + 1);
}

string getAppName()
/*
Function that returns file path to a currently using application
*/
{
    HWND hwnd = GetForegroundWindow(); // Get currently using application
    DWORD pid;
    GetWindowThreadProcessId(hwnd, &pid); // Get it pid

    HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, pid); // Open a process that get information about app
    if (!hProcess)
        return "Unknown"; // If process doesn't exist, just return "Unknown"

    char title[256];
    GetModuleFileNameExA(hProcess, nullptr, title, sizeof(title)); // Save file path to application

    CloseHandle(hProcess); // Closes the process

    return string(title); // Returns file path to currently using application
}

bool checkIfExistsInVector(vector<string> vector_to_check, string newApp)
/*
Function that returns if the value is already in vector
*/
{
    if (find(vector_to_check.begin(), vector_to_check.end(), newApp) == vector_to_check.end())
    {
        return false;
    }
    else
    {
        return true;
    }
}

void printAllApps(vector<string> all_apps, map<string, int> appTimes)
/*
Function that is used to print all of the data out at once
*/
{
    for (int i = 0; i < (int)all_apps.size(); i++)
    {
        cout << all_apps[i] << ": " << changeTimeFormat(appTimes[all_apps[i]]) << endl;
    }
}

int main()
{
    // Initializing main variables
    map<string, int> base; // Variable for all the apps with their seconds in usage
    map<string, string> times; // Variable for all the apps and their last time usage
    vector<string> apps; // Variable for all the apps names
    while (true)
    {

        string currentApp = getFileName(getAppName()); // Getting currently used application
        times[currentApp] = getTime(); // Updating 'last time used' variable
        if (base.find(currentApp) != base.end())
        {
            // If app was already launched

            base[currentApp] += 1; // Add a second to usage time
        }
        else
        {
            // If app wasn't launched yet

            base[currentApp] = 0; // Add usage variable to it
            if (!checkIfExistsInVector(apps, currentApp))
            {
                // If app isn't in the 'apps list'

                apps.push_back(currentApp); // Add it to a list
            }
        }

        saveData(base, times); // Saves the data to file

        this_thread::sleep_for(chrono::seconds(1)); // Wait a second between another refresh
    }
    return 0;
}
