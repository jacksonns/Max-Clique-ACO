from src.aco import AntColonyOptimizer
import multiprocessing

EXEC_NUM = 30

#FILE_PATH = "datasets/p_hat700-2.clq.txt"
FILE_PATH = "datasets/brock800_4.clq.txt"
#RESULTS_ROOT = "results_phat"
RESULTS_ROOT = "results_brock"

def test_ants_num(ant_num):
    result_path = f'{RESULTS_ROOT}/600it{ant_num}ants.txt'
    config_args = {
        "ants_num": ant_num,
        "iterations": 600,
        "evaporation": 0.8,
        "alpha": 1,
        "file_path": FILE_PATH,
        "results_path": result_path
    }
    
    aco = AntColonyOptimizer(config_args)

    print(f'\nExecuting {EXEC_NUM} times for ants_num={ant_num}')
    for i in range(EXEC_NUM):
        print(f'Execução {i}')
        aco.run()
    
    aco.results.write_results(EXEC_NUM)


def test_alpha_rho(alpha_rho):
    alpha, rho = alpha_rho

    result_path = f'{RESULTS_ROOT}/alpha{alpha}rho{rho}.txt'
    config_args = {
        "ants_num": 30,
        "iterations": 400,
        "evaporation": rho,
        "alpha": alpha,
        "file_path": FILE_PATH,
        "results_path": result_path
    }
    
    aco = AntColonyOptimizer(config_args)

    print(f'\nExecuting {EXEC_NUM} times for alpha={alpha}, rho={rho}')
    for i in range(EXEC_NUM):
        print(f'Execução {i}')
        aco.run()
    
    aco.results.write_results(EXEC_NUM)


if __name__ == '__main__':
    ants_num = [5, 10, 15, 20, 30]
    alpha_rho_list = [(1, 0.80), (1, 0.90), (1, 0.99), (2, 0.80), (2, 0.90), (2, 0.99)]

    with multiprocessing.Pool() as pool:
        #pool.map(test_ants_num, ants_num)
        pool.map(test_alpha_rho, alpha_rho_list)
