"""Exercise a rendered native two-ledger transaction, without field writes."""


def supports(game):
    return (game is not None and type(game).__module__.startswith('saga.mini.')
        and all(callable(getattr(game,name,None)) for name in ('push','put','get','end'))
        and type(getattr(game,'cash',None)) in (int,float)
        and type(getattr(game,'bank',None)) in (int,float))


def step(game, nodes, receipt, run):
    """Deposit one unit, withdraw it, then use the actual exit button."""
    if not supports(game):return False
    def rendered(function,args):
        matches=[]
        for node in nodes:
            sensitive=getattr(node,'is_sensitive',None)
            if not callable(sensitive) or not sensitive():continue
            action=getattr(node,'clicked',None)
            if action is function and not args:
                matches.append(action)
                continue
            callback=getattr(action,'callable',action)
            if callback==function and tuple(getattr(action,'args',()))==args and not getattr(action,'kwargs',{}):
                matches.append(action)
        if not matches:raise ValueError('Native wallet input is not rendered and sensitive')
        return matches[0]
    phase=receipt.get('phase',0)
    if phase==0:
        if game.cash<1 or game.bank<0:raise ValueError('Native wallet needs a positive test denomination')
        if str(getattr(game,'delta','')) not in ('','0'):raise ValueError('Native wallet input is not initially empty')
        receipt.update(before={'cash':game.cash,'bank':game.bank},phase=1,inputs=[])
        action=rendered(game.push,('1',))
        receipt['inputs'].append('1')
    elif phase==1:
        action=rendered(game.put,())
        receipt['inputs'].append('deposit')
        receipt['phase']=2
    elif phase==2:
        before=receipt['before']
        if (game.cash,game.bank)!=(before['cash']-1,before['bank']+1):
            raise ValueError('Native deposit did not produce the requested ledger transition')
        receipt['after_deposit']={'cash':game.cash,'bank':game.bank}
        action=rendered(game.push,('1',))
        receipt['inputs'].append('1')
        receipt['phase']=3
    elif phase==3:
        action=rendered(game.get,())
        receipt['inputs'].append('withdraw')
        receipt['phase']=4
    elif phase==4:
        before=receipt['before']
        if (game.cash,game.bank)!=(before['cash'],before['bank']):
            raise ValueError('Native withdrawal did not restore both ledgers')
        receipt['after_withdrawal']={'cash':game.cash,'bank':game.bank}
        action=rendered(game.end,())
        receipt['inputs'].append('exit')
        receipt['phase']=5
        receipt['game_local_ledger_validated']=True
    else:raise ValueError('Native wallet exit did not return to its caller')
    run(action)
    return True
