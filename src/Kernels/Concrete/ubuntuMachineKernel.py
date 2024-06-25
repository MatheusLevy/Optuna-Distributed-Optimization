from Kernels.Exceptions.MachineKernelException import MachineKernelException
from Kernels.Strategy.machineKernel import MachineKernel
import paramiko

class UbuntoMachineKernel(MachineKernel):
    def __init__(self,
                 username,
                 password,
                 host='localhost',
                 ssh_port=22
                 ):
        self.username= username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            self.ssh.connect(
                hostname=host,
                port=ssh_port,
                username=username,
                password=password
            )
        except Exception as e:
            raise MachineKernelException(
                mensage="Erro connecting to machine",
                details=f"Failed to connect to {host}:{ssh_port}",
                error=e
            ) from e
        
    def get_partition_info(self, partition="/"):
        cmd = f'df -h | awk \'$6 == "{partition}"\''
        try:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
        except Exception as e:
            raise MachineKernelException(
                mensage="Erro executing command",
                details=f"Failed to run command: {cmd}",
                error=e
            ) from e
        out = stdout.read().decode()
        error = stderr.read().decode()
        parts = out.split()
        partition_info = {
            "device": parts[0],
            "total_size": parts[1],
            "used_space": parts[2],
            "free_space": parts[3],
            "porcent_used": parts[4],
            "mounted_at":parts[5],
            "errors": error
        }
        return partition_info
    
    def get_memmory_info(self):
        cmd = 'free -h'
        try:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
        except Exception as e:
            raise MachineKernelException(
                mensage="Erro executing command",
                details=f"Failed to run command: {cmd}",
                error=e
            ) from e
        out = stdout.read().decode()
        error = stderr.read().decode()
        parts_memory = out.splitlines()[1].split()
        parts_swap = out.splitlines()[2].split()
        memory_info = {
            "total_memory": parts_memory[1],
            "used_memory": parts_memory[2],
            "free_memory": parts_memory[3],
            "shared_memory": parts_memory[4],
            "buffer_cache": parts_memory[5],
            "available": parts_memory[6],
            "total_swap": parts_swap[1],
            "used_swap": parts_swap[2],
            "free_swap": parts_swap[3],
            "errors":error
        }
        return memory_info
        
    def get_CPU_info(self):
        cmd1 = 'lscpu'
        cmd2 = 'top -bn1 | head -n10'
        try:
            stdin_lscpu, stdout_lscpu, stderr_lscpu = self.ssh.exec_command(cmd1)
            stdin_top, stdout_top, stderr_top = self.ssh.exec_command(cmd2)
        except Exception as e:
            raise MachineKernelException(
                mensage="Erro executing command",
                details=f"Failed to run commands: {cmd1} or {cmd2}",
                error=e
            ) from e
        out_lscpu = stdout_lscpu.read().decode()
        error_lscpu = stderr_lscpu.read().decode()
        out_top = stdout_top.read().decode()
        error_top = stdout_top.read().decode()

        lines_lscpu = out_lscpu.splitlines()
        cpu_cores = lines_lscpu[7].split(sep=":")[1]
        thred_per_core = lines_lscpu[8].split(sep=":")[1]
        cpu_threds = str(int(cpu_cores) * int(thred_per_core))
        lines_top = out_top.splitlines()[7:]
        processes_using_cpu  = []
        for line in lines_top:
            line_split = line.split()
            pid = line_split[0]
            user = line_split[1]
            cpu_use = line_split[8]
            mem_use = line_split[9]
            time = line_split[10]
            command= line_split[11]
            processes_using_cpu.append({
                "pid": pid,
                "user": user,
                "cpu_use": cpu_use,
                "memmory_use": mem_use,
                "time": time,
                "command": command
            })
        cpu_info = {
            "cpu_cores": cpu_cores,
            "cpu_threads": cpu_threds,
            "processes": processes_using_cpu,
            "erorrs": [stderr_top, stderr_lscpu]
        }
        return cpu_info
    
    def get_GPU_info(self):
        cmd1 = "nvidia-smi -L"
        try:
            stdin_vga, stdout_vga, stderr_vga = self.ssh.exec_command(cmd1)
        except Exception as e:
            raise MachineKernelException(
                mensage="Erro executing command",
                details=f"Failed to run command: {cmd1}",
                error=e
            ) from e
        out = stdout_vga.read().decode()
        error = stderr_vga.read().decode()
        vgas = out.splitlines()
        gpu_info = [
        ]

        for vga in vgas:

            vga_infos = dict()
            splited_infos = vga.split(sep=":")
            gpu_id = splited_infos[0].split()[1]
            model = splited_infos[1]
            cut_position = model.find("(")
            if cut_position != -1:
                model = model[:cut_position].strip()
            
            vga_infos["gpu_id"] = gpu_id
            vga_infos["model"] = model
            cmd_usage = f"nvidia-smi -i {gpu_id}"

            try:
                stdin, stdout, stderr = self.ssh.exec_command(cmd_usage)
            except Exception as e:
                raise MachineKernelException(
                    mensage="Erro retrieving gpu info",
                    details=f"Failed to run {cmd_usage}",
                    error=e
                ) from e
            out= stdout.read().decode()
            error = stderr.read().decode()

            nvidia_gpu_info = out.splitlines()[9]
            usage= nvidia_gpu_info.split()[1]
            temp = nvidia_gpu_info.split()[2]
            current_watts = nvidia_gpu_info.split()[4]
            max_watts = nvidia_gpu_info.split()[6]
            used_vram= nvidia_gpu_info.split()[8]
            max_vram = nvidia_gpu_info.split()[10]
            gpu_usage = nvidia_gpu_info.split()[12]

            vga_infos["usage"] = usage
            vga_infos["temp"] = temp
            vga_infos["current_watts"] = current_watts
            vga_infos["max_watts"] = max_watts
            vga_infos["used_vram"] = used_vram
            vga_infos["max_vram"] = max_vram
            vga_infos["gpu_usage"] = gpu_usage
            vga_infos["process"] = []
            nvidia_gpu_process_infos = out.splitlines()[18:]
            nvidia_gpu_process_infos = nvidia_gpu_process_infos[:len(nvidia_gpu_process_infos)-1]
            for line in nvidia_gpu_process_infos:
                splited = line.split()
                gpu_id_on_process = splited[1]
                pid = splited[4]
                process_name =splited[6]
                gpu_memory_usage =splited[7]
                process_info = {
                    "gpu_id": gpu_id_on_process,
                    "pid": pid,
                    "memmory_usage": gpu_memory_usage,
                    "process_name": process_name
                }
                vga_infos["process"].append(process_info)
        gpu_info.append(vga_infos)
        return gpu_info


    def get_process_info(self, pid):
        return super().get_process_info(pid)
    
    def get_process_on_gpu(self):
        return super().get_process_on_gpu()
    
    def kill_process_info(self, pid):
        return super().kill_process_info(pid)
    
    def gpu_is_used(self):
        return super().gpu_is_used()