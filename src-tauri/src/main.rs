// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

extern crate winapi;
use std::thread;
use std::time::Duration;
use winapi::{
    shared::minwindef::FILETIME,
    um::{
        processthreadsapi::GetSystemTimes,
        sysinfoapi::{GetSystemInfo, GlobalMemoryStatusEx, MEMORYSTATUSEX, SYSTEM_INFO},
    },
};

// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
#[tauri::command]
fn cpu_count() -> u32 {
    unsafe {
        let mut sys_info: SYSTEM_INFO = std::mem::zeroed();
        GetSystemInfo(&mut sys_info);
        sys_info.dwNumberOfProcessors
    }
}

#[tauri::command]
fn memory() -> u64 {
    unsafe {
        let mut mem_status: MEMORYSTATUSEX = std::mem::zeroed();
        mem_status.dwLength = std::mem::size_of::<MEMORYSTATUSEX>() as u32;

        if GlobalMemoryStatusEx(&mut mem_status) != 0 {
            mem_status.ullAvailPhys / mem_status.ullTotalPhys
        } else {
            0
        }
    }
}

#[tauri::command]
fn cpu() -> f64 {
    unsafe {
        let mut idle_time = FILETIME {
            dwLowDateTime: 0,
            dwHighDateTime: 0,
        };
        let mut kernel_time = FILETIME {
            dwLowDateTime: 0,
            dwHighDateTime: 0,
        };
        let mut user_time = FILETIME {
            dwLowDateTime: 0,
            dwHighDateTime: 0,
        };

        if GetSystemTimes(&mut idle_time, &mut kernel_time, &mut user_time) == 0 {
            return 0.0;
        }

        thread::sleep(Duration::from_secs(1));

        let prev_idle_time = idle_time;
        let prev_kernel_time = kernel_time;
        let prev_user_time = user_time;

        if GetSystemTimes(&mut idle_time, &mut kernel_time, &mut user_time) == 0 {
            return 0.0;
        }

        let idle_time_diff = filetime_to_u64(idle_time) - filetime_to_u64(prev_idle_time);
        let kernel_time_diff = filetime_to_u64(kernel_time) - filetime_to_u64(prev_kernel_time);
        let user_time_diff = filetime_to_u64(user_time) - filetime_to_u64(prev_user_time);

        let total_time_diff = kernel_time_diff + user_time_diff;

        let cpu_usage = if total_time_diff > 0 {
            (total_time_diff - idle_time_diff) as f64 / total_time_diff as f64
        } else {
            0.0
        };

        cpu_usage
    }
}

fn filetime_to_u64(ft: FILETIME) -> u64 {
    ((ft.dwHighDateTime as u64) << 32) | (ft.dwLowDateTime as u64)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![cpu_count, memory, cpu])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
