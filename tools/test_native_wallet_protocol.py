import unittest
from types import SimpleNamespace as NS
from native_tests.native_wallet_protocol import step


class Wallet:
    __module__='saga.mini.wallet_fixture'
    def __init__(self):self.cash,self.bank,self.delta,self.exited=10,0,'',False
    def push(self,digit):self.delta+=digit
    def put(self):
        amount=int(self.delta)
        self.cash-=amount
        self.bank+=amount
        self.delta=''
    def get(self):
        amount=int(self.delta)
        self.cash+=amount
        self.bank-=amount
        self.delta=''
    def end(self):self.exited=True


class WalletProtocol(unittest.TestCase):
    def test_native_stored_action_objects_keep_identity_and_arguments(self):
        class Action:
            def __init__(self,callback,*args):self.callable,self.args,self.kwargs=callback,args,{}
            def __call__(self):self.callable(*self.args)
        game=Wallet()
        put,get,end=game.put,game.get,game.end
        game.put,game.get,game.end=Action(put),Action(get),Action(end)
        receipt={}
        for unused in range(5):step(game,self.controls(game),receipt,self.execute_action)
        self.assertTrue(game.exited)
        self.assertEqual((game.cash,game.bank),(10,0))
    def controls(self,game):
        push=NS(callable=game.push,args=('1',),kwargs={})
        return [NS(clicked=action,is_sensitive=lambda:True) for action in (push,game.put,game.get,game.end)]
    def execute_action(self,action):
        callback=getattr(action,'callable',action)
        callback(*getattr(action,'args',()))
    def test_actual_transaction_and_exit_restore_both_ledgers(self):
        game,receipt=Wallet(),{}
        for unused in range(5):step(game,self.controls(game),receipt,self.execute_action)
        self.assertEqual(receipt['after_deposit'],{'cash':9,'bank':1})
        self.assertEqual(receipt['after_withdrawal'],{'cash':10,'bank':0})
        self.assertTrue(game.exited)
        self.assertNotIn('native_caller_commit_validated',receipt)
    def test_missing_native_deposit_button_does_not_invoke_method(self):
        game,receipt=Wallet(),{}
        step(game,self.controls(game),receipt,self.execute_action)
        with self.assertRaisesRegex(ValueError,'not rendered'):
            step(game,[],receipt,self.execute_action)
        self.assertEqual((game.cash,game.bank),(10,0))
    def test_changed_transaction_semantics_fail_closed(self):
        game,receipt=Wallet(),{}
        step(game,self.controls(game),receipt,self.execute_action)
        step(game,self.controls(game),receipt,self.execute_action)
        game.cash-=1
        with self.assertRaisesRegex(ValueError,'ledger transition'):
            step(game,self.controls(game),receipt,self.execute_action)


if __name__=='__main__':unittest.main()
