import os
import sys
import argparse
import subprocess
import shutil
from datetime import datetime
from function.print_log import log


class TestRunner:
    def __init__(self):
        # 项目根目录
        self.project_root = os.path.dirname(os.path.abspath(__file__))

        # 目录配置
        self.case_dir = os.path.join(self.project_root, "case")
        self.allure_results_dir = os.path.join(self.project_root, "allure_results")
        self.allure_reports_dir = os.path.join(self.project_root, "allure_reports")

        # 确保目录存在
        self._ensure_dirs()

    def _ensure_dirs(self):
        """确保必要目录存在"""
        for dir_path in [self.allure_results_dir, self.allure_reports_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                log.info(f'创建了{dir_path}目录')


    def _clean_old_results(self):
        """清理旧的 allure 结果"""
        if os.path.exists(self.allure_results_dir):
            shutil.rmtree(self.allure_results_dir)
            log.info('已清理旧的allure结果，并创建了新的allure结果目录')
        os.makedirs(self.allure_results_dir)

    def _get_test_files(self):
        """获取所有可用的测试文件"""
        test_files = []
        if os.path.exists(self.case_dir):
            for file in os.listdir(self.case_dir):
                if file.startswith("test_") and file.endswith(".py"):
                    test_files.append(file)
        return sorted(test_files) # 排序的作用是确保每次返回的顺序是一致的

    def _build_pytest_cmd(self, test_file=None, markers=None, verbosity="v"):
        """
        构建 pytest 命令参数

        Args:
            test_file: 指定测试文件 (如: test_sys.py)
            markers: 指定标记 (如: "smoke" 或 "smoke or regression")
            verbosity: 详细程度 (v, vv, vvv)
        """
        cmd = [
            "-s",  # 捕获输出
            f"-{verbosity}",  # 详细程度
            "--alluredir", self.allure_results_dir,  # allure 结果目录
            "--clean-alluredir",  # 清理旧的 allure 结果
        ]

        # 构建测试路径
        if test_file:
            if not test_file.endswith(".py"):
                test_file += ".py"
            test_path = os.path.join(self.case_dir, test_file)
            if not os.path.exists(test_path):
                log.error(f"错误: 测试文件不存在: {test_path}")
                sys.exit(1)
            cmd.append(test_path)
            log.info(f"指定测试文件: {test_file}")
        else:
            cmd.append(self.case_dir)
            log.info("运行所有测试文件")

        # 添加标记过滤
        if markers:
            cmd.extend(["-m", markers])
            log.info(f"指定标记: {markers}")

        log.info(f'已构建好的命令组合为{cmd}')
        return cmd

    def run_testcase(self, test_file=None, markers=None, verbosity="v"):
        """
        运行测试

        Args:
            test_file: 指定测试文件
            markers: pytest 标记过滤
            verbosity: 详细程度
        """
        # 清理旧结果
        self._clean_old_results()

        log.info('开始运行测试！')

        # 构建并执行 pytest 命令
        pytest_args = self._build_pytest_cmd(test_file, markers, verbosity)

        # 使用 sys.executable 确保使用当前 Python 环境
        cmd = [sys.executable, "-m", "pytest"] + pytest_args

        log.info(f"执行命令为: {' '.join(cmd)}\n")

        # 运行测试
        result = subprocess.run(cmd, cwd=self.project_root,shell=True)
        log.info('开始执行测试！')

        return result.returncode

    def generate_report(self, serve=False):
        """
        生成 Allure 报告x

        Args:
            serve: 是否启动本地服务器查看报告
        """
        print(f"\n{'=' * 50}")
        print("生成 Allure 报告...")
        print(f"{'=' * 50}\n")

        if serve:
            # 启动本地服务器
            log.info(f"启动 Allure 报告服务...\n 结果目录: {self.allure_results_dir}")
            cmd = ["allure", "serve", self.allure_results_dir]
            log.info(f'动态allure命令为{cmd}')
        else:
            # 生成静态报告
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_dir = os.path.join(self.allure_reports_dir, f"report_{timestamp}")

            log.info(f"生成静态报告输出目录: {report_dir}")
            cmd = [
                "allure", "generate",
                self.allure_results_dir,
                "-o", report_dir,
                "--clean"
            ]

        try:
            log.info('开始尝试生成allure报告！')
            subprocess.run(cmd, cwd=self.project_root,shell=True)
            if not serve:
                log.info(f"报告生成成功!\n 报告路径: {report_dir}")
            return True
        except Exception as e:
            log.error(f"生成报告失败: {e}")
            return False

    def list_test_files(self):
        """列出所有可用的测试文件"""
        print("可用的测试文件:")
        print("-" * 40)
        test_files = self._get_test_files()
        if test_files:
            for i, f in enumerate(test_files, 1):
                print(f"  {i}. {f}")
        else:
            print("  (未找到测试文件)")
        print("-" * 40)


def main():
    parser = argparse.ArgumentParser(
        description="BaseApiTest 接口自动化测试启动器",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # 测试文件选择
    parser.add_argument(
        "-f", "--file",
        help="指定测试文件 (如: test_sys.py，不需要完整路径)"
    )

    # 标记过滤
    parser.add_argument(
        "-m", "--markers",
        help="pytest 标记过滤 (如: smoke, regression, 'smoke or regression')"
    )

    # 详细程度
    parser.add_argument(
        "-v", "--verbosity",
        choices=["v", "vv", "vvv"],
        default="v",
        help="输出详细程度 (默认: v)"
    )

    # 报告选项
    # Jenkins命令启动时，不要用-s在线打开报告，会导致程序卡主不往下执行

    report_group = parser.add_mutually_exclusive_group()
    report_group.add_argument(
        "-s", "--serve",
        action="store_true",
        help="运行后启动 Allure 本地服务查看报告"
    )
    report_group.add_argument(
        "-r","--report-only",
        action="store_true",
        help="仅生成报告（不运行测试，使用已有的allure_results）"
    )

    # 列出测试文件
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="列出所有可用的测试文件"
    )

    args = parser.parse_args()

    runner = TestRunner()

    # 列出测试文件
    if args.list:
        runner.list_test_files()


    # 不执行测试，仅用上次测试完的结果来生成报告
    if args.report_only:
        runner.generate_report(serve=args.serve)



    # 运行测试
    exit_code = runner.run_testcase(
        test_file = args.file,
        markers = args.markers,
        verbosity = args.verbosity
    )

    log.warning(f'这是args.serve的值{args.serve}')

    # 生成报告
    if exit_code == 0 or exit_code == 1:  # 0=成功, 1=部分测试失败
        runner.generate_report(serve = args.serve)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()




