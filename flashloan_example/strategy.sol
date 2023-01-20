pragma solidity ^0.6.6;
import { ILendingPoolAddressesProvider } from "./ILendingPoolAddressesProvider.sol"; 
import { FlashLoanReceiverBase } from "./FlashLoanReceiverBase.sol";  
import { ILendingPool } from "./ILendingPool.sol";        
import { IERC20 } from "./IERC20.sol";                   



contract MyfirstFlashLoan is FlashLoanReceiverBase {

    /**
        在你的策略合约收到闪电贷金额后将调用此函数
     */
    function executeOperation(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata premiums,
        address initiator,
        bytes calldata params
    )
        external
        override
        returns (bool)
    {

        // 该策略合约此时已获得所需资金
        // 策略逻辑可以写在这里
        
        // 在上述逻辑的最后，该合约欠闪电贷额度 + 手续费。
        // 因此，请确保您的合同有足够的资金来偿还这些金额。
        
        // 授权 LendingPool 合约提前欠款额度
        for (uint i = 0; i < assets.length; i++) {
            uint amountOwing = amounts[i].add(premiums[i]);
            IERC20(assets[i]).approve(address(LENDING_POOL), amountOwing);
        }
        
        return true;
    }
    
    function myfirstFlashLoanCall() public {
        // 接收贷款地址
        address receiverAddress = address(this);

        // 贷款币币种,仅贷一个币种
        address[] memory assets = new address[](1);
        assets[0] = address(INSERT_ASSET_ONE_ADDRESS);

        // 贷款币数量
        uint256[] memory amounts = new uint256[](1);
        amounts[0] = INSERT_ASSET_ONE_AMOUNT;

        // 贷款模式
        uint256[] memory modes = new uint256[](1);
        modes[0] = INSERT_ASSET_ONE_MODE;

        address onBehalfOf = address(this);
        bytes memory params = "";
        uint16 referralCode = 0;

        LENDING_POOL.flashLoan(
            receiverAddress,
            assets,
            amounts,
            modes,
            onBehalfOf,
            params,
            referralCode
        );
    }
}