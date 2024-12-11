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
    - PC1 -> 192.168.0.1/24
    - PC2 -> 192.168.0.2/24
    - PC3 -> 192.168.0.3/24
    - PC4 -> 192.168.0.4/24

    ![image](https://github.com/user-attachments/assets/65371431-ce95-40ba-94d7-5ca964b3d4d9)

2. Foi adicionado os ips a cada computador da seguinte forma:

    ![image](https://github.com/user-attachments/assets/e0fe4aa1-1d8c-4415-a07b-d83b5c8c2f85)


3. No swtich os computadores estão conectados nas seguintes interfaces:
    1. PC1 - F1/1
    2. PC2 - F1/2
    3. PC3 - F1/3
    4. PC4 - F1/4

4.  No swtich foi digitado os seguintes comandos no **CLI**:

    *Obs: VLAN 1 já vem configurada por default*
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
5. No cmd do PC1, foi feitos os seguintes pings:
    - PC1 para PC2 - OK
    - PC1 para PC3 - FAIL
      
      ![image](https://github.com/user-attachments/assets/56778973-4c51-4954-872b-e30c1cfe4984)


## Exercicio 2
