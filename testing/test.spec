#SYNTAX EXAMPLE
#<set>:<callerName>:<methodName>:<arg1>,<arg2>:<True:False>
#<assert>:<callerName>:<methodName>:<arg1>,<arg2>:<returnValue>
#arguments may reference a callerAddress by placing a $ in front of callerName
#you may select all callers to perform this action by setting $* as callerName
#you can select all but one caller by setting caller as $!<callerName>
#the same logic works for $ prefixed arguments
#if using $* or $!, all permutations of ident and args will be called

#BASE STATE TESTS
    #assert that owner is owner
    assert:None:isOwner:$owner:True
    #assert that no one else is owner
    assert:None:isOwner:$!owner:False
    #assert the failsafe is failsafe
    assert:None:isFailsafe:$failsafe:True
    #assert that no one else is failsafe
    assert:None:isFailsafe:$!failsafe:False
    #assert that everyones balance is zero
    assert:None:balanceOf:$*:0
    #assert that no one is an authority
    assert:None:isAuthority:$*:False
    #assert that no one is a vault
    assert:None:isVault:$*:False

#VERIFY OWNER AND FAILSAFE ABILITY TO SET OWNER AND FAILSAFE
    #owner can set owner
    set:owner:setOwner:$owner:True
    #failsafe can set owner
    set:failsafe:setOwner:$owner:True
    #owner can not set failsafe
    set:owner:setFailsafe:$owner:False
    #failsafe can set failsafe
    set:failsafe:setFailsafe:$failsafe:True

#TEST OWNER AND FAILSAFE AUTHORITY ACTIONS
    #owner can add an authority
    set:owner:addAuthority:$authority1:True
    #authority1 is now an authority
    assert:None:isAuthority:$authority1:True
    #failsafe can add an authority
    set:failsafe:addAuthority:$authority2:True
    #authority2 is now an authority
    assert:None:isAuthority:$authority2:True

#VERIFY AUTHORITIES AND NON-AUTHORITIES CAN NOT ADD AN AUTHORITY
    #authorities can not add authorities
    set:authority1:addAuthority:$authority3:False
    #non-authorities can not add authorities
    set:token1:addAuthority:$authority3:False
    #prove that authority3 is not an authority1
    assert:None:isAuthority:$authority3:False

#VERIFY OWNER AND FAILSAFE VAULT METHODS
    #owner can set a vault
    set:owner:addVault:$vault1:True
    #verify vault is set
    assert:None:isVault:$vault1:True
    #failsafe can set a vault
    set:failsafe:addVault:$vault2:True
    #verify vault is set
    assert:None:isVault:$vault2:True

#VERIFY NO ONE ELSE CAN SET A VAULT
    #authorities can not add vaults
    set:authority1:addVault:$vault3:False
    #vault is not set
    assert:None:isVault:$vault3:False
    #non-authorities/vaults can not add vaults
    set:token1:addVault:$vault3:False
    #vault is not set
    assert:None:isVault:$vault3:False
    #vaults can not add vaults
    set:vault1:addVault:$vault3:False
    #vault is not set
    assert:None:isVault:$vault3:False

#TEST THAT AN AUTHORITY/VAULT CAN CREATE/CLEAR A DESPOSIT AND SUPPLIES WORK
    assert:None:totalSupply::0
    assert:None:pendingSupply::0
    assert:None:availableSupply::0
    set:authority1:deposit:$token1,100:True
    assert:None:pendingSupply::100
    assert:None:totalSupply::100
    assert:None:availableSupply::0
    set:vault1:releaseDeposit:$token1,100:True
    assert:None:balanceOf:$token1:100
    assert:None:pendingSupply::0
    assert:None:totalSupply::100
    assert:None:availableSupply::100

#TEST THAT AN AUTHORITY/VAULT CAN CREATE/REVOKE A DESPOSIT
    set:authority1:deposit:$token1,100:True
    assert:None:pendingSupply::100
    assert:None:totalSupply::200
    assert:None:availableSupply::100
    set:vault1:revokeDeposit:$token1,100:True
    assert:None:pendingSupply::0
    assert:None:totalSupply::100
    assert:None:availableSupply::100
    assert:None:balanceOf:$token1:100

#TEST THAT A VAULT CAN NOT CLEAR OR REVOKE A WITHOUT A PENDING DESPOSIT
    set:vault1:releaseDeposit:$token1,100:False
    set:vault1:revokeDeposit:$token1,100:False
    assert:None:balanceOf:$token1:100
    assert:None:pendingSupply::0
    assert:None:totalSupply::100
    assert:None:availableSupply::100

#TEST TRANSFERS OF TOKENS
    set:$!token1:transfer:$token1,1:False
    set:token1:transfer:$!token1,1:True
    assert:None:balanceOf:$!token1:1
    set:$!token1:transfer:$token1,1:True
    assert:None:balanceOf:$!token1:0
    assert:None:balanceOf:$token1:100
    set:$!token1:transfer:$token1,1000:False
    assert:None:balanceOf:$!token1:0
    assert:None:balanceOf:$token1:100
    assert:None:pendingSupply::0
    assert:None:totalSupply::100
    assert:None:availableSupply::100

#TEST WITHDRAW OF TOKENS
#NOTE: require(registration) IS COMMENTED OUT IN WITHDRAW TO TEST THIS
    set:token1:withdraw:1:True
    assert:None:balanceOf:$token1:99
    assert:None:pendingSupply::0
    assert:None:totalSupply::99
    assert:None:availableSupply::99
    assert:None:balanceOf:$token2:0
    set:token2:withdraw:1:False
    assert:None:balanceOf:$token2:0
    assert:None:pendingSupply::0
    assert:None:totalSupply::99
    assert:None:availableSupply::99

#TEST REMOVAL OF VAULTS
    set:None:removeVault:$vault1:False
    set:vault1:removeVault:$vault1:False
    set:authority1:removeVault:$vault1:False
    assert:None:isVault:$vault1:True
    set:owner:removeVault:$vault1:True
    assert:None:isVault:$vault1:False
    set:failsafe:removeVault:$vault2:True
    assert:None:isVault:$vault2:False

#TEST REMOVAL OF AUTHORITIES
    set:None:removeAuthority:$authority1:False
    set:vault1:removeAuthority:$authority1:False
    set:authority1:removeAuthority:$authority1:False
    assert:None:isAuthority:$authority1:True
    set:owner:removeAuthority:$authority1:True
    assert:None:isAuthority:$authority1:False
    set:failsafe:removeAuthority:$authority2:True
    assert:None:isAuthority:$authority2:False

#TEST DEPOSITS BY PRIOR AUTHORITIES
    assert:None:totalSupply::99
    assert:None:availableSupply::99
    assert:None:pendingSupply::0
    set:authority1:deposit:$token1,100:False
    assert:None:totalSupply::99
    assert:None:availableSupply::99
    assert:None:pendingSupply::0

#TEST CLEARANCE ABILITY OF PRIOR AUTHORITIES
    set:owner:addAuthority:$authority3:True
    set:owner:addVault:$vault3:True
    set:authority3:deposit:$token1,1:True
    assert:None:totalSupply::100
    assert:None:availableSupply::99
    assert:None:pendingSupply::1
    set:vault1:releaseDeposit:$token1,1:False
    assert:None:totalSupply::100
    assert:None:availableSupply::99
    assert:None:pendingSupply::1
    set:vault3:releaseDeposit:$token1,1:True
    assert:None:totalSupply::100
    assert:None:availableSupply::100
    assert:None:pendingSupply::0

#TEST ALLOWNACE METHODS
    set:token1:approve:$token2,1:True
    assert:None:allowance:$token1,$token2:1
    set:token2:transferFrom:$token1,$token2,1:True
    assert:None:balanceOf:$token2:1
    set:token2:transfer:$token1,1:True
    assert:None:balanceOf:$token2:0
    set:token1:approve:$token2,1:True
    set:token1:increaseAllowance:$token2,1:True
    assert:None:allowance:$token1,$token2:2
    set:token2:transferFrom:$token1,$token2,2:True
    assert:None:balanceOf:$token2:2
    set:token2:transfer:$token1,2:True
    assert:None:balanceOf:$token2:0
    set:token1:approve:$token2,1:True
    set:token1:decreaseAllowance:$token2,1:True
    assert:None:allowance:$token1,$token2:0
    set:token2:transferFrom:$token1,$token2,1:False
    assert:None:balanceOf:$token2:0
    set:token1:approve:$token2,1:True

#TEST REGISTRATION AND UNREGISTRATION
    set:owner:addAuthority:0x372422a22712ab41c7067dbc36447296776e0de3:True
    set:dev:register:0x0000000000000000000000000000000000000000000000000000000000abc123,28,0x736e83159093e711ed7bbd431018d27015440494bd1c405280e2935cebc65392,0x2cad662685907a6b7ac51bd3b093823f355ff09a25c55dc2a2a3e5ea2c7984ad:True
    assert:None:isRegistered:$dev:True
    set:authority3:unregister:$dev:True
    assert:None:isRegistered:$dev:False

#TEST CONTRACT PAUSE
    assert:None:isPaused::False
    set:owner:pause::True
    assert:None:isPaused::True

#TEST ALL METHODS LOCKED IN PAUSE
    set:owner:addAuthority:$authority1:False
    set:owner:addVault:$vault1:False
    set:token1:transfer:$token2,1:False
    set:token1:approve:$token2,1:False
    set:token2:transferFrom:$token1,$token2,1:False
    set:token1:increaseAllowance:$token2,1:False
    set:token1:decreaseAllowance:$token2,1:False
    set:token1:withdraw:1:False
    set:authority1:deposit:$token1,1:False

#TEST ONLY FAILSAFE CAN UNPAUSE
    assert:None:isPaused::True
    set:$!failsafe:unpause::False
    set:failsafe:unpause::True
    assert:None:isPaused::False

#TEST LOCKDOWN NOTE: THIS MUST BE DONE LAST!
    assert:None:isPaused::False
    set:$!failsafe:lockForever::False
    set:failsafe:lockForever::True
    assert:None:isPaused::True
    set:$*:unpause::False
    assert:None:isPaused::True
