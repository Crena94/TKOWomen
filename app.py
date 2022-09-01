import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('1/Activities/04-Stu_Certificate_dApp/Solved/contracts/compiled/fighter_abi.json')) as f:
        fighter_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Load the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=fighter_abi
    )

    return contract

contract = load_contract()


################################################################################
# Register New Artwork
################################################################################
st.title("Choose your Fighter!")

from PIL import Image

image1 = Image.open("fighter_1.jpg")
image2 = Image.open("fighter_2.jpg")
image3 = Image.open("fighter_3.jpg")
image4 = Image.open("fighter_4.jpg")
image5 = Image.open("fighter_5.jpg")
image6 = Image.open("fighter_6.jpg")

st.image([image1,image2,image3,image4,image5,image6], caption = ["Fighter 1", "Fighter 2", "Fighter 3", "Fighter 4", "Fighter 5", "Fighter 6"], width = 100)

selected_fighter = st.selectbox("Which Fighter would you like to purchase?", options = [1,2,3,4,5,6])

if selected_fighter == 1:
    fighter_uri = "https://gateway.pinata.cloud/ipfs/QmVPWMD4mUXN77FgNKTeBEfefyTJwXscrTBuumRJX7Rd2u/02.jpg"
    
elif selected_fighter ==2:
    fighter_uri = "https://gateway.pinata.cloud/ipfs/QmVPWMD4mUXN77FgNKTeBEfefyTJwXscrTBuumRJX7Rd2u/04.jpg"
    
elif selected_fighter == 3:
    fighter_uri = "https://gateway.pinata.cloud/ipfs/QmVPWMD4mUXN77FgNKTeBEfefyTJwXscrTBuumRJX7Rd2u/114.jpg"
    
elif selected_fighter == 4:
    fighter_uri = "https://gateway.pinata.cloud/ipfs/QmVPWMD4mUXN77FgNKTeBEfefyTJwXscrTBuumRJX7Rd2u/15.jpg"
    
elif selected_fighter == 5:
    fighter_uri = "https://gateway.pinata.cloud/ipfs/QmVPWMD4mUXN77FgNKTeBEfefyTJwXscrTBuumRJX7Rd2u/1613.jpg"
    
elif selected_fighter == 6:
    fighter_uri = "https://gateway.pinata.cloud/ipfs/QmVPWMD4mUXN77FgNKTeBEfefyTJwXscrTBuumRJX7Rd2u/1764.jpg"
    
accounts = w3.eth.accounts
# Use a streamlit component to get the address of the artwork owner from the user
address = st.selectbox("Select address to purchase Fighter", options=accounts)

# Use a streamlit component to get the artwork's URI


if st.button("Register Fighter"):
    # Use the contract to send a transaction to the registerArtwork function
    tx_hash = contract.functions.registerFighter(
        address,
        fighter_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    
    

st.markdown("---")

################################################################################
# Display a Token
################################################################################
st.markdown("## Display an Art Token")

selected_address = st.selectbox("Select Account", options=accounts)

tokens = contract.functions.balanceOf(selected_address).call()

st.write(f"This address owns {tokens} fighters.")

token_id = st.selectbox("Owned Fighters", list(range(tokens)))


if st.button("Display Fighter"):
    # Use the contract's `ownerOf` function to get the art token owner
    owner = contract.functions.ownerOf(token_id).call()
    
    st.write(f"The token is registered to {owner}")

    # Use the contract's `tokenURI` function to get the art token's URI
    token_uri = contract.functions.tokenURI(token_id).call()

    st.write(f"{token_uri}")
    st.image(token_uri)

