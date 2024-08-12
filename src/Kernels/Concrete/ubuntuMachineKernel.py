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
        self.host = host
        try:
            self.ssh.connect(
                hostname=host,
                port=ssh_port,
                username=username,
                password=password
            )
        except Exception as e:
            raise MachineKernelException(
                message="Erro connecting to machine",
                details=f"Failed to connect to {host}:{ssh_port}",
                error=e
            ) from e
    
    def get_partition_info(self, partition="/"):
        def _build_partition_dict(stdout, stderr):
            out = stdout.read().decode()
            error = stderr.read().decode()
            parts = out.split()
            return {
                "device": parts[0],
                "total_size": parts[1],
                "used_space": parts[2],
                "free_space": parts[3],
                "porcent_used": parts[4],
                "mounted_at":parts[5],
                "errors": error
            }
        
        cmd = f'df -B1 | awk \'$6 == "{partition}"\''
        try:
            _, stdout, stderr = self.ssh.exec_command(cmd)
        except Exception as e:
            raise MachineKernelException(
                message="Erro executing command",
                details=f"Failed to run command: {cmd}",
                error=e
            ) from e
        print(stdout)
        return _build_partition_dict(stdout, stderr)

    def get_memmory_info(self):
        def _build_memmory_inf(stdout, stderr):
            def _split_out_componets(out):
                out_lines = out.splitlines()
                memory_info_line = out_lines[1]
                swap_info_line = out_lines[0]
                memory_infos = memory_info_line.split()
                swap_infos = swap_info_line.split()
                return memory_infos, swap_infos
            
            out = stdout.read().decode()
            error = stderr.read().decode()
            memory_infos, swap_infos = _split_out_componets(out)

            return {
                "total_memory": memory_infos[1],
                "used_memory": memory_infos[2],
                "free_memory": memory_infos[3],
                "shared_memory": memory_infos[4],
                "buffer_cache": memory_infos[5],
                "available": memory_infos[6],
                "total_swap": swap_infos[1],
                "used_swap": swap_infos[2],
                "free_swap": swap_infos[3],
                "errors":error
            }
        
        cmd = 'free -h'
        try:
            _, stdout, stderr = self.ssh.exec_command(cmd)
        except Exception as e:
            raise MachineKernelException(
                message="Erro executing command",
                details=f"Failed to run command: {cmd}",
                error=e
            ) from e
        return _build_memmory_inf(stdout, stderr)
    

    def get_CPU_info(self):
        def build_cpu_info(stdout, stderr):
            out = stdout.read().decode()
            error = stderr.read().decode()
            out_lines = out.splitlines()

            cpu_cores=  out_lines[7].split(sep=":")[1]
            thred_per_core = out_lines[8].split(sep=":")[1]
            cpu_threds = str(int(cpu_cores) * int(thred_per_core))
            
            return {
                "cpu_cores": cpu_cores,
                "cpu_threads": cpu_threds,
                "erorrs": error
            }
        
        def build_process_info(stdout, stderr):
            out = stdout.read().decode()
            error = stderr.read().decode()
            out_lines = out.splitlines()[7:]
            processes_in_cpu = []
            for process_line in out_lines:
                process_infos = process_line.split()
                processes_in_cpu.append({
                "pid": process_infos[0],
                "user": process_infos[1],
                "cpu_use": process_infos[8],
                "memmory_use": process_infos[9],
                "time": process_infos[10],
                "command": process_infos[11],
                "error": error
            })
            return processes_in_cpu

        def exec_commands(self, commands):
            responses = []
            for command in commands:
                _, stdout, stderr = self.ssh.exec_command(command)
                responses.append({
                        "command": command,
                        "stdout": stdout,
                        "stderr": stderr
                    })
            return responses
       
        cmd1 = 'lscpu'
        cmd2 = 'top -bn1 | head -n10'
        try:
            responses = exec_commands(self, [cmd1, cmd2])
        except Exception as e:
            raise MachineKernelException(
                message="Erro executing command",
                details=f"Failed to run commands: {cmd1} or {cmd2}",
                error=e
            ) from e
        
        cpu_info = dict()
        process_info = []
        for response in responses:
            command = response['command']
            if  command == cmd1:
                cpu_info = build_cpu_info(response['stdout'], response['stderr'])
            if command == cmd2:
                process_info = build_process_info(response['stdout'], response["stderr"])
        
        cpu_info['processes'] = process_info
        return cpu_info
    
    def get_GPU_info(self):
        def build_vgas_infos(stdout, stderr):
            def get_gpus_infos(gpus):
                def extract_gpu_model(string):
                    cut_position = string.find("(")
                    if cut_position != -1:
                        string = string[:cut_position].strip()
                    return string
                def extract_id(gpu_infos):
                    return  gpu_infos[0].split()[1]

                infos = []
                for gpu in gpus:
                    gpu_infos = gpu.split(sep=":")
                    infos.append({
                        "id":extract_id(gpu_infos),
                        "model": extract_gpu_model(gpu_infos[1]),
                    })
                return infos

            out = stdout.read().decode()
            error = stderr.read().decode()
            gpus = out.splitlines()
            return get_gpus_infos(gpus)
        
        def extract_extra_infos(out, error):
            gpu_info_line = out.splitlines()[9]
            gpu_infos = gpu_info_line.split()
            return {
                "usage": gpu_infos[1],
                "temp": gpu_infos[2],
                "current_watts": gpu_infos[4],
                "max_watts": gpu_infos[6],
                "used_vram": gpu_infos[8],
                "max_vram": gpu_infos[10],
                "gpu_usage": gpu_infos[12],
                "error": error
            }
        def extract_process_infos(out, error):

            processes_lines = out.splitlines()[18:]
            processes_lines = processes_lines[:len(processes_lines)-1] 
            processes = []
            for process_line in processes_lines:
                process_infos = process_line.split()
                processes.append({
                    'gpu_id': process_infos[1],
                    "pid": process_infos[4],
                    "process_name": process_infos[6],
                    "memmory_usage": process_infos[7],
                    "error": error
                })
            return processes


        cmd1 = "nvidia-smi -L"
        try:
            _, stdout, stderr = self.ssh.exec_command(cmd1)
        except Exception as e:
            raise MachineKernelException(
                message="Erro executing command",
                details=f"Failed to run command: {cmd1}",
                error=e
            ) from e
        gpus_info = build_vgas_infos(stdout, stderr)
        for gpu in gpus_info:
            cmd_usage = f"nvidia-smi -i {gpu['id']}"
            try:
                _, stdout, stderr = self.ssh.exec_command(cmd_usage)
            except Exception as e:
                raise MachineKernelException(
                    message="Erro retrieving gpu info",
                    details=f"Failed to run {cmd_usage}",
                    error=e
                ) from e
            out= stdout.read().decode()
            error = stderr.read().decode()
            extra_infos = extract_extra_infos(out, error)
            processes_infos = extract_process_infos(out, error)
            gpu['extra'] = extra_infos
            gpu['process'] = processes_infos
        return gpus_info


    def get_process_info(self, pid):
        def build_process_info(stdout, stderr):
            out= stdout.read().decode()
            error = stderr.read().decode()
            process_info = out.splitlines()[1]
            process_infos = process_info.split()
            print(process_infos)
            return {
                "pid": process_infos[0],
                "ppid": process_infos[1],
                "cmd": process_infos[2],
                "cpu_usage": process_infos[3],
                "memory_usage": process_infos[4],
                "etime": process_infos[5],
                "error": error
            }
        
        cmd = f"ps -p {pid} -o pid,ppid,cmd,%cpu,%mem,etime"
        try:
            _, stdout, stderr = self.ssh.exec_command(cmd)
        except Exception as e:
            raise MachineKernelException(
                message="Erro executing command",
                details=f"Failed to run command: {cmd}",
                error=e
            ) from e
        return build_process_info(stdout, stderr)
    
    def kill_process_info(self, pid):
        cmd = f"kill {pid}; echo 'KILL'"
        try:
            _, _, stderr = self.ssh.exec_command(cmd)
        except Exception as e:
            raise MachineKernelException(
                message="Erro executing command",
                details=f"Failed to run command: {cmd}",
                error=e
            ) from e
        return stderr.read().decode()
    
    def gpu_is_used(self):
        def extract_mb_usage(string):
            return int(string.replace('MiB',''))
        
        gpus = self.get_GPU_info()
        for gpu in gpus:
            for process in gpu['process']:
                gpu['in_use'] = extract_mb_usage(process['memmory_usage']) > 500
        return gpus
    
    def get_folder_size(self, path_to_folder):
        cmd = f"du -sb {path_to_folder}"
        try:
            _, stdout, stderr = self.ssh.exec_command(cmd)
        except Exception as e:
            raise MachineKernelException(
                message="Erro executing command",
                details=f"Failed to run command: {cmd}",
                error=e
            ) from e
        return stdout.read().decode().split('\t')[0]