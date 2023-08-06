def parse_resources(params):
    if type(params) == str:
        return {
            "instance_type": params,
            "instance_count": 1
        }
    elif 'instance' in params:
        return {
            'instance_type': params['instance_type'],
            'instance_count': params['instance_count']
        }
    elif 'cpu' in params:
        return {
            'cpu': params['cpu'],
            'memory': params['memory']
        }

def parse_infrastructure(params):
    '''
    Parse the infrastructure section of the provider YAML
    and assess the actual provider that this type of job should use.

    If there is only one provider in the infrastructure section, 
    it will be used for all jobs. Else, it will feed jobs the specific provider (SageMaker, AzureML, etc).
    '''

       # TODO: add validation on allowed infrastructure
    options = ['process', 'train', 'deploy', 'batch']
    infra_options = {}
    # loop through the infra options
    # if no job_type, mark it as the default
    for infra in params:

        # parse through the current infra_option
        # print(infra)
        iter = {'name': infra['name']}
        iter['container_repo'] = infra['container_repo']

        # currently used for AWS
        if 'arn' in infra:
            iter['arn'] = infra['arn']

        # currently used for Azure
        if 'resource_group' in infra:
            iter['resource_group'] = infra['resource_group']
        
        if 'workspace_name' in infra:
            iter['workspace_name'] = infra['workspace_name']
        
        # selection of instance type and resources in k8s/AWS SM
        if 'resources' in infra:
            iter['resources'] = parse_resources(infra['resources'])
        
        if 'job_type' in infra:
            # if selected, save the infra for a specific type
            
            for job in infra['job_type']:
                # save the infra choice for a job type
                if job in options:
                    infra_options[job] = iter
                else:
                    print(f'{job} in an invalid job type in provider yaml.')
        
        else: 
            # else save as the default option
            infra_options['default'] = iter
    
    # if there's a default, copy it over to the other jobs
    if 'default' in infra_options:
        for job in options:
            # save default infra job to all other
            if job not in infra_options:
                # print(f'Copying default infra config to {job}')
                infra_options[job] = infra_options['default']

    # print(infra_options)

    # if hosting add in autoscaling params
    if ('resources' in infra_options['deploy'] and
        'instance_type' in infra_options['deploy']['resources'] and 
        'instance_count_max' not in infra_options['deploy']['resources']):
        infra_options['deploy']['resources']['instance_count_max'] = 1
        
    return infra_options