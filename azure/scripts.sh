az ad sp create-for-rbac \
  --name "github-actions-sp" \
  --role contributor \
  --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/pacocha-az \
  --json-auth

# run this to get acces to the azure project for github 
# ad sp -> create principal service, like a credential
# create-for-rbac -> create a service principal and assign a role to it (RBAC -> Role-Based Access Control)
# --name -> is just the name 
# --role contributor -> can create delete and modify resources
# --scopes  -> the scope so just the porject
# --json-auth -> output the credentials in json format
