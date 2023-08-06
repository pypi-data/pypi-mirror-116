import re
import onnxruntime
from .adaptive_batch_size import adaptive_batch_size
from .gpu_scheduler import get_gpu_info, get_gpu_utilization, get_gpumem_utilization

def get_device_id(device):
    pattern = re.compile(r'\d+')
    try:    
        span = re.search(pattern, device).span() 
        dv_id = int(device[span[0]:span[1]])
    except:
        dv_id = 0
    return dv_id

def generate_device(device_list, type = 'gpu'):
    device = ''
    for dl in device_list:
        if len(dl) != 0:
            if type == 'gpu':
                device = 'cuda: {}'.format(dl[0]) 
                break
    if device == '':
        device = 'cpu'
    return device

def get_provider_new(device = None):
    batch_size = 1
    d_cuda = ('CUDAExecutionProvider',{
              'device_id': 0,
              'arena_extend_strategy': 'kNextPowerOfTwo',
              'cudnn_conv_algo_search': 'EXHAUSTIVE',
              'cuda_mem_limit': 1<<30
            })
    d_cpu = ('CPUExecutionProvider',{})
    if 'CUDAExecutionProvider' not in onnxruntime.get_available_providers():
        return [d_cpu], False, batch_size
    fp16_mode = False

    comp_usable = [i['gpu_id'] for i in get_gpu_utilization() if i['gpu_rate'] <0.2]
    mem_usable = [i['gpu_id'] for i in get_gpumem_utilization() if i['mem_rate'] >0.7]
    gpu_usable = list(set(comp_usable).intersection(set(mem_usable)))
    fp16_device = [i['gpu_id'] for i in get_gpu_info(gpu_usable) if i['gpu_compt']>=6.1]
    device_list = [fp16_device, gpu_usable]
    
    if device == None:
        device = generate_device(device_list)
    
    if 'cpu' in device:
        providers = [d_cpu]
        batch_size = 1
    elif 'cuda' in device:
        d_cuda[1]['device_id'] = get_device_id(device)
        if d_cuda[1]['device_id'] in fp16_device:
            fp16_mode = True
        batch_size, mem_avl = adaptive_batch_size(d_cuda[1]['device_id'], fp16_mode)    
        d_cuda[1]['cuda_mem_limit'] = mem_avl <<30
        providers = [d_cuda, d_cpu]

    return providers, fp16_mode, batch_size

def get_provider(device = None):
    providers, fp16_mode, batch_size = get_provider_new(device)
    provider = [i[0] for i in providers]
    provider_op = [i[1] for i in providers]
    provider_op = [{key: str(value) for (key, value) in d.items()} for d in provider_op]
    return provider, provider_op, fp16_mode, batch_size
