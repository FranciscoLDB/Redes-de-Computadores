## Exercicio 1
1. Divida o switch em 2 VLANs.
    1. Professores: VLAN 1 (portas 1 e 2)
    2. Alunos: VLAN 2 (portas 3 e 4)
    3. Faça as VLANS se comunicarem entre si.
        1. Teste utilizando o ping para verificar a comunicação entre máquinas
            1. VLAN1 com VLAN1
            2. VLAN1 com VLAN2

### Passo a Passo
1. Criar os recursos:
    - Todos computadores estão na rede 192.168.0.0/24
        | Máquina | IP          | Máscara       |
        |---------|-------------|---------------|
        | PC1     | 192.168.0.1 | 255.255.255.0 |
        | PC2     | 192.168.0.2 | 255.255.255.0 |
        | PC3     | 192.168.0.3 | 255.255.255.0 |
        | PC4     | 192.168.0.4 | 255.255.255.0 |

    ![image](https://github.com/user-attachments/assets/0c04ce96-bb41-44be-a1b4-4fa223eb653f)

2. Foi adicionado os ips a cada computador da seguinte forma:

    ![image](https://github.com/user-attachments/assets/e0fe4aa1-1d8c-4415-a07b-d83b5c8c2f85)


3. No swtich os computadores estão conectados nas seguintes interfaces:
    | Switch  | Máquina | Porta  |
    |---------|---------|--------|
    | SWT1    | PC1    | F1/1   |
    | SWT1    | PC2    | F2/1   |
    | SWT1    | PC3    | F3/1   |
    | SWT1    | PC4    | F4/1   |

5.  No swtich foi digitado os seguintes comandos no **CLI**:

    *Obs: VLAN 1 já vem configurada por default*
    - Cria VLAN 2
    - Configura portas 1 e 2 para vlan1
    - Configura portas 3 e 4 para vlan2
    ```
    Swtich> enable
    Swtich# confi t
    Swtich(config)# vlan 2
    Swtich(config-vlan)# name VLAN-2
    Swtich(config-vlan)# exit
    
    Swtich(config)# int f1/1
    Swtich(config-if)# switchport access vlan1
    Swtich(config)# int f2/1
    Swtich(config-if)# switchport access vlan1
    
    Swtich(config)# int f3/1
    Swtich(config-if)# switchport access vlan2
    Swtich(config)# int f4/1
    Swtich(config-if)# switchport access vlan2
    Swtich(config-if)# end
    Swtich# exit
    Swtich>  
     ```
6. No cmd do PC1, foi feitos os seguintes pings:
    - PC1 para PC2 - OK
    - PC1 para PC3 - FAIL
      
      ![image](https://github.com/user-attachments/assets/56778973-4c51-4954-872b-e30c1cfe4984)

## Exercicio 2
1. Divida o switch em 2 VLANs.
    1. Professores: VLAN 1 (portas 1 e 2)
    2. Alunos: VLAN 2 (portas 3 e 4)
    3. Faça as VLANS se comunicarem entre si.
        1. Teste utilizando o ping para verificar a comunicação entre máquinas
    4. Ao terminar coloque todas as máquinas na VLAN 1
        1. VLAN1 com VLAN1 (No mesmo switch)
        2. VLAN1 com VLAN2 (No mesmo switch)
        3. VLAN1 com VLAN1 (Em switchs diferentes)
        4. VLAN1 com VLAN2 (Em switchs diferentes)

### Passo a Passo
1. Criar os recursos:
    - Foi criado os computadores, swtichs e conectados pelos cabos.
    - Foi adicionado os ips para cada computador.
    - Computadores na rede 192.168.0.0/24
        | Máquina | IP           | Máscara       |
        |---------|--------------|---------------|
        | PC10    | 192.168.0.10 | 255.255.255.0 |
        | PC20    | 192.168.0.20 | 255.255.255.0 |
        | PC30    | 192.168.0.30 | 255.255.255.0 |
        | PC40    | 192.168.0.40 | 255.255.255.0 |

    - Computadores na rede 192.168.0.0/24
        | Máquina | IP           | Máscara       |
        |---------|--------------|---------------|
        | PC50    | 192.168.0.50 | 255.255.255.0 |
        | PC60    | 192.168.0.60 | 255.255.255.0 |
        | PC70    | 192.168.0.70 | 255.255.255.0 |
        | PC80    | 192.168.0.80 | 255.255.255.0 |

    ![image](https://github.com/user-attachments/assets/1ff17eca-6d24-401a-8e04-5aa051eb19e4)

2. Nos swtichs os computadores estão conectados nas seguintes interfaces:
    1. Swtich SWT10:

        | Máquina | Porta  |
        |---------|--------|
        | SWT30   | F0/1   |
        | PC10    | F1/1   |
        | PC20    | F2/1   |
        | PC30    | F3/1   |
        | PC40    | F4/1   |
       
    2. Swtich SWT20:

        | Máquina | Porta  |
        |---------|--------|
        | SWT30   | F0/1   |
        | PC50    | F1/1   |
        | PC60    | F2/1   |
        | PC70    | F3/1   |
        | PC80    | F4/1   |
       
    3. Swtich SWT30:

        | Máquina | Porta  |
        |---------|--------|
        | SWT10   | F1/1   |
        | SWT20   | F2/1   |
   
3. No Switch da Rede 1 e da Rede 2:
    *Obs: VLAN 1 já vem configurada por default*
    - Cria VLAN 2
    - Configura portas 1 e 2 para vlan1
    - Configura portas 3 e 4 para vlan2
    - Configura porta 0 para vlan1 e vlan2 (modo trunk)
    ```
    Swtich> enable
    Swtich# confi t
    Swtich(config)# vlan 2
    Swtich(config-vlan)# name VLAN-2
    Swtich(config-vlan)# exit
    
    Swtich(config)# int f1/1
    Swtich(config-if)# switchport access vlan1
    Swtich(config)# int f2/1
    Swtich(config-if)# switchport access vlan1
    
    Swtich(config)# int f3/1
    Swtich(config-if)# switchport access vlan2
    Swtich(config)# int f4/1
    Swtich(config-if)# switchport access vlan2

    Swtich(config)# int f0/1
    Swtich(config-if)# switchport mode trunk
    Swtich(config-if)# switchport trunk allowed vlan add 1
    Swtich(config-if)# switchport trunk allowed vlan add 2
    Swtich(config-if)# end
    Swtich# exit
    Swtich>  
     ```

4. No Switch intermediário:
    *Obs: VLAN 1 já vem configurada por default*
    - Cria VLAN 2
    - Configura porta 1 para vlan1 e vlan2 (modo trunk)
    - Configura porta 2 para vlan1 e vlan2 (modo trunk)
    ```
    Swtich> enable
    Swtich# confi t
    Swtich(config)# vlan 2
    Swtich(config-vlan)# name VLAN-2
    Swtich(config-vlan)# exit
    
    Swtich(config)# int f1/1
    Swtich(config-if)# switchport mode trunk
    Swtich(config-if)# switchport trunk allowed vlan add 1
    Swtich(config-if)# switchport trunk allowed vlan add 2

    Swtich(config)# int f2/1
    Swtich(config-if)# switchport mode trunk
    Swtich(config-if)# switchport trunk allowed vlan add 1
    Swtich(config-if)# switchport trunk allowed vlan add 2
    Swtich(config-if)# end
    Swtich# exit
    Swtich>  
     ```

5. Pings
    1. VLAN1 com VLAN1 (No mesmo switch)
        - PC10 -> PC20
       
           ![image](https://github.com/user-attachments/assets/c634724f-4d05-408f-be96-3ff30cf8a290)
        
    2. VLAN1 com VLAN2 (No mesmo switch)
        - PC10 -> PC30
       
           ![image](https://github.com/user-attachments/assets/e8809223-09eb-4a88-bd0a-a672722d390e)
          
    3. VLAN1 com VLAN1 (Em switchs diferentes)
        - PC10 -> PC50
       
          ![image](https://github.com/user-attachments/assets/4a2e114c-092d-488d-bc29-ab4190a0855d)

    4. VLAN1 com VLAN2 (Em switchs diferentes)
        - PC10 -> PC70
       
          ![image](https://github.com/user-attachments/assets/75b1b79d-cd13-4e12-8c70-b32dd524919f)

6. Alterando tudo para VLAN 1:
    *Obs: VLAN 1 já vem configurada por default*
    - Configura portas 3 e 4 para vlan1
    - As portas 1 e 2 já estão na vlan1
    ```
    Swtich> enable
    Swtich# confi t
    Swtich(config)# int f3/1
    Swtich(config-if)# switchport access vlan2
    Swtich(config)# int f4/1
    Swtich(config-if)# switchport access vlan2
    Swtich(config-if)# end
    Swtich# exit
    Swtich>  
     ```

7. Pings
    1. VLAN1 com VLAN1 (No mesmo switch)
        - PC10 -> PC20
       
           ![image](https://github.com/user-attachments/assets/17e19a9f-342b-41cc-bcdf-7d886c911da7)
        
    2. VLAN1 com VLAN1 (No mesmo switch)
        - PC10 -> PC30
       
           ![image](https://github.com/user-attachments/assets/c1a8e5ee-21be-4b51-aa04-41f8fc961e77)
          
    3. VLAN1 com VLAN1 (Em switchs diferentes)
        - PC10 -> PC50
       
          ![image](https://github.com/user-attachments/assets/4a2e114c-092d-488d-bc29-ab4190a0855d)

    4. VLAN1 com VLAN1 (Em switchs diferentes)
        - PC10 -> PC70
       
          ![image](https://github.com/user-attachments/assets/d76f31d8-52c2-48f4-a037-eae68e929e85)
