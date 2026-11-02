class TodoItem:
    def __init__(self, title:str, is_completed:bool=False ):
        self.title = title
        self.is_completed = is_completed

    def mark_done(self):
        self.is_completed = True

    def __str__(self):
        status = "[✓]" if self.is_completed else "[ ]"
        return f"{status} {self.title}"

class TodoList:
    def __init__(self):
        self.items = []
    
    def add_task(self, title:str):
        self.items.append(TodoItem(title))        

    def show_tasks(self):
        if len(self.items) == 0:
            print("当前暂无待办事项")
        else:
            for index, task in enumerate(self.items, start=1):
                # print(f"{index}. task name:  {task.title}. status: {"已完成" if task.is_completed else "未完成"}")
                print(f"{index}. {task}")

    def complete_task(self, index:int):
        if index < 1:
            print("完成的任务序号错误")
        else:
            self.items[index-1].mark_done()

    def delete_task(self, index:int):
        if index < 1:
            print("删除的任务序号错误")
        else:
            del self.items[index-1]
    
def main():
    todo_app = TodoList()
    print("start")

    while True:
        print("""============================ 
            1. 查看所有任务 (Show)
            2. 添加待办任务 (Add) 
            3. 标记完成任务 (Done)
            4. 删除待办任务 (Delete)
            5. 退出程序 (Exit)
            ============================
        """)
        choice = input("请选择操作编号")
        match choice:
            case "1":
                todo_app.show_tasks()
            case "2":
                task = input("请输入任务内容")
                todo_app.add_task(task)
            case "3":
                index = input("请输入要完成的任务")
                print(f"你输入了： {index}")
                task_index = check(index, todo_app.items)
                if task_index == -1:
                    print("输入的数字无对应任务编号")
                elif task_index == -2:
                    print("输入有误，不能转换为整数！")
                else:
                    todo_app.complete_task(task_index)
                
            case "4":
                index = input("请输入要删除的任务")
                task_index = check(index, todo_app.items)
                if task_index == -1:
                    print("输入的数字无对应任务编号")
                elif task_index == -2:
                    print("输入有误，不能转换为整数！")
                else:
                    todo_app.delete_task(task_index)
                
            case "5":
                print("bye bye")
                break
            case _:
                print("无效输入，请重新选择")

def check(index:str, todo_app:list) -> int:
    try:
        print(f"index: {index}")
        task_index = int(index.strip())
        if task_index > 0 and task_index <= len(todo_app):
            return task_index
        else:
            return -1
    except Exception as e:
        print(f"Error: {e}")
        return -2

if __name__ == "__main__":
    main()