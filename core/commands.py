from abc import ABC, abstractmethod

class Command(ABC):
    """Abstract base class for all commands."""
    
    @abstractmethod
    def execute(self):
        """Execute the command."""
        pass

    @abstractmethod
    def undo(self):
        """Undo the command."""
        pass

class CommandInvoker:
    """Invoker to manage command execution, undo, and redo."""
    
    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def execute_command(self, command: Command):
        """Executes a command and pushes it to the undo stack."""
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear() # Clear redo stack on new action

    def undo(self):
        """Undoes the last command."""
        if not self._undo_stack:
            return False
        
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)
        return True

    def redo(self):
        """Redoes the last undone command."""
        if not self._redo_stack:
            return False
            
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)
        return True
    
    def can_undo(self):
        return len(self._undo_stack) > 0
    
    def can_redo(self):
        return len(self._redo_stack) > 0
